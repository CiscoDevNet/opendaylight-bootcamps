'''
Created on Jan 22, 2016

@author: Bluesy Wang
'''

from exception.embedder_exception import *
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from argparse import ArgumentParser
import threading
import json
import logging as log
from settings import network_configuration
from basics.flow_install import FlowInstaller
from basics.topo_aware import TopoMonitor
from basics.replica_compute import ReplicaComputer


class ERROR_CODE:
    PARSE_ERROR = -32700          # Invalid JSON was received by the server.
    INVALID_REQ = -32600          # The JSON sent is not a valid Request object.
    METHOD_NOT_FOUND = -32601     # The method does not exist / is not available.
    INVALID_PARAMS = -32602       # Invalid method parameter(s).
    INTERNAL_ERROR = -32603          # Internal JSON-RPC error.


class FLRClient():
    def __init__(self, odlhost, odlport, odluser, odlpassword):
        self.odlhost = odlhost
        self.odlport = odlport
        self.odluser = odluser
        self.odlpassword = odlpassword
        self.base_url = "http://%s:%s/restconf/" % (self.odlhost, self.odlport)
        self.base_flowid = '1'
        self.odl_base_flowpriority = '10'
        
        if network_configuration.odl_server_user.strip():
            self.odluser = network_configuration.odl_server_user
        if network_configuration.odl_server_password.strip():
            self.odlpassword = network_configuration.odl_server_password
        if network_configuration.odl_server_url_prefix.strip():
            self.base_url = network_configuration.odl_server_url_prefix
        if network_configuration.odl_base_flowid.strip():
            self.base_flowid = network_configuration.odl_base_flowid
        if network_configuration.odl_base_flowpriority.strip():
            self.odl_base_flowpriority = network_configuration.odl_base_flowpriority
    
    def startup(self):
        replicacompute = ReplicaComputer(FlowInstaller(self.odluser, self.odlpassword, self.base_url, 
                             self.base_flowid, self.odl_base_flowpriority))
        topomonitor = TopoMonitor(replicacompute)
        topomonitor.run()
        
        

class FLREmbedderHandler(BaseHTTPRequestHandler):
    """
    Implementation of JSON-RPC API, defines all API handler methods.
    """
  
    def _buildResponse(self, json_id, result=None, error=None):
        """Returns JSON 2.0 compliant response"""
        res = {}
        res['jsonrpc'] = '2.0'
        # result and error are mutually exclusive
        if result is not None:
            res['result'] = result
        elif error is not None:
            res['error'] = error
        res['id'] = json_id
        return res

    def _buildError(self, code, message, data=None):
        """Returns JSON RPC 2.0 error object"""
        res = {}
        res['code'] = code
        res['message'] = message
        if data:
            res['data'] = data
        return res    

    def do_POST(self):
        """Handle HTTP POST calls"""

        def reply(response):
            response = json.dumps(response) + '\n'
            self.send_response(200, "OK")
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(response))
            self.end_headers()
            self.wfile.write(response)
    
        # Put JSON message in data dict
        l = self.headers.get("Content-Length", "")
        data = ''
        if l == "":
            data = self.rfile.read()
        else:
            data = self.rfile.read(int(l))
        try:
            data = json.loads(data)
        except:
            msg = "Error parsing JSON request"
            log.error(msg)
            err = self._buildError(ERROR_CODE.PARSE_ERROR, msg)
            result = self._buildResponse(None, error=err)
            reply(result)
        # Check if JSONRPC 2.0 compliant (correct version and json_id given)
        json_id = data.get('id', None)
        # Setup method to call
        try:
            methodName = "_exec_" + data.get('method')
            method = getattr(self, methodName)
            log.info(methodName)
        except:
            msg = "Method not found"
            log.info(msg)
            err = self._buildError(ERROR_CODE.METHOD_NOT_FOUND, msg)
            result = self._buildResponse(json_id, error=err)
            reply(result)
        # Get method parameters
        params = data.get('params', {})
        # Call method
        result = method(json_id, params)

        reply(result)
    
    
    #TODO
    def _exec_modifyConfiguration(self, json_id, params):
        """Handler for modify ODL-FLR configuration"""
        try:
            p = params.get('config')
            if p == None:
                raise EmbedderException(ERROR_CODE.INVALID_REQ, 'Missing configuration section')
            #else
                #TODO
            response = self._buildResponse(json_id, result={ 'status' : 'success' })
        except EmbedderException as e:
            log.error(e)
            err = self._buildError(e.code, e.msg)
            response = self._buildResponse(json_id, error=err)
        return response


class FLREmbedderServer(HTTPServer):
    def __init__(self, opts):
        HTTPServer.__init__(self, (opts['host'], opts['port']), FLREmbedderHandler)


class FLREmbedder(threading.Thread):
    """
    ODL-FLR JSON RPC 2.0 server
    """
    def __init__(self, opts):
        threading.Thread.__init__(self)
        self.httpd = FLREmbedderServer(opts)
        self.setDaemon(True)
    
    # Multi-threaded webserver
    def run(self):
        """
        Main function run by thread
        """
        log.info("JSON RPC server starting")
        try:
            self.httpd.serve_forever()
        finally:
            self.httpd.server_close()


if __name__ == '__main__':
    parser = ArgumentParser(description="ODL-FLR embedding tool.")
    parser.add_argument('--host', default='localhost', help='ODL-FLR embedder host (default="localhost")')
    parser.add_argument('--port', default=8000, type=int, help='ODL-FLR embedder port (default=8000)')
    parser.add_argument('--odlhost', default='localhost', help='host where OpenDaylight is running (default="localhost")')
    parser.add_argument('--odlport', default=8181, type=int, help='port where OpenDaylight RestConf is running (default=8080)')
    parser.add_argument('--odluser', default='admin', help='OpenDaylisht user (default="admin")')
    parser.add_argument('--odlpass', default='admin', help='OpenDaylight password (default="admin")')
    parser.add_argument('--loglevel', default='INFO', help='log level (default="INFO")')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    opts = vars(args)
  
    log.basicConfig(format='%(asctime)s %(message)s', level=getattr(log, opts['loglevel'].upper()))
    
    client = FLRClient(opts['odlhost'], opts['odlport'], opts['odluser'], opts['odlpass'])
    
    client.startup()
    
#     flowinstaller.installflow({"node-id":"openflow:1","table-id":"0","flow-id":"odl-1","in-port":"1",
#         "dl-src":"00:00:00:00:00:01","dl-dst":"00:00:00:00:00:02","out-port":"2"})
#     flowinstaller.installflow({"node-id":"openflow:1","table-id":"0","flow-id":"odl-2","in-port":"1",
#         "dl-src":"00:00:00:00:00:01","dl-dst":"00:00:00:00:00:02","out-port":"2"})
    
    embedder = FLREmbedder(opts)
    embedder.run()
    
    