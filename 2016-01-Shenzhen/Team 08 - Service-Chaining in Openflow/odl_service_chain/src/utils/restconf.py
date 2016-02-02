import logging
import requests
import jsonutils
import base64

LOG = logging.getLogger(__name__)


DEFAULT_HTTP_REQUEST_TIMEOUT = 20
ODL_USER = "admin"
ODL_PASSWORD = "admin"
ODL_RESTCONF_URL = "restconf"
ODL_CFG_URL = "config/"
ODL_OPER_URL = "operational/"
ODL_RPC_URL = "operations/"
ODL_TOPO_URL = "network-topology:network-topology"
ODL_NODE_URL = "topology-netconf:node/"

class AuthBase(object):
    def getAuth(self):
        pass

class HttpAuthBase(AuthBase):
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def _getBaseAuthHdr(self):
        base64string = base64.encodestring('%s:%s' % (self.user, self.password))[:-1]
        authheader =  "Basic %s" % base64string
        return authheader

    def getAuth(self):
        return self._getBaseAuthHdr()

class HttpRequestBase(object):

    def __init__(self, url, auth, timeout=0):
        self.url = url
        self.auth = auth
        self.timeout=timeout

    def sendjson(self, method, urlpath, obj):
        headers = {'Content-Type': 'application/json'}
        url = '/'.join([self.url, urlpath])

        log_msg = "Sending METHOD (%(method)s) URL (%(url)s) JSON (%(obj)s)"%({'method': method, 'url': url, 'obj': obj})
        LOG.info(log_msg)

        if method=="get":
            r = requests.get(url,headers=headers, auth=self.auth)
        elif method == "post":
            data = jsonutils.dumps(obj, indent=2) if obj else None
            r = requests.post(url,data,headers=headers, auth=self.auth)

        if r.status_code >= 200 or r.status_code < 299:
            return r
        else:
            r.raise_for_status()


class ODLRestRequest(HttpRequestBase):
    def __init__(self, ipaddr, port=8181):
        self.timeout = DEFAULT_HTTP_REQUEST_TIMEOUT
        self.user = ODL_USER
        self.password = ODL_PASSWORD
        self.controller_ip = ipaddr
        self.controller_port = port
        self.controller_url = "http://"+self.controller_ip + ":"+str(self.controller_port)
        self.base_url = self.controller_url + "/" + ODL_RESTCONF_URL
        self.auth = (self.user, self.password)
        super(ODLRestRequest,self).__init__(self.base_url, self.auth, self.timeout)

    def _create_resource(self, rsc_url, rsc_body):
        response = self.sendjson("post", rsc_url, rsc_body)
        return response

    def _get_resource(self, rsc_url, rsc_body):
        response = self.sendjson("get", rsc_url, rsc_body)
        return response.content

    def list_openflow_nodes(self):
        urlpath = ODL_OPER_URL + "opendaylight-inventory:nodes/"
        print("list_openflow_nodes: url_path--- " + urlpath)
        openflowNodesStr = self._get_resource(urlpath,None)
        node_list = jsonutils.loads(openflowNodesStr)["nodes"]["node"]
        return node_list

    def get_openflow_topology(self):
        urlpath = ODL_OPER_URL +"/" + ODL_TOPO_URL
        print("get_openlow_topology: url_path--- " + urlpath)
        topoStr = self._get_resource(urlpath, None)
        topology_list = jsonutils.loads(topoStr)["network-topology"]["topology"]
        return topology_list[0]

    def config_openflow(self,ctrl_ip, flowRsc):
        flow_url = "/".join(["http://"+ctrl_ip+":8181", ODL_RESTCONF_URL,ODL_RPC_URL,"sal-flow:add-flow"])
        headers={"Content-type":"application/xml"}
        response = requests.post(flow_url, flowRsc,headers=headers, auth=self.auth)
        print(response.status_code)
        print(response.content)
        return response