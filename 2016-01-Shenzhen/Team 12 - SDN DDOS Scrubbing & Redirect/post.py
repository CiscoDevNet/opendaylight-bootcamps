
from __future__ import print_function
from sys import stderr
from basics import odl_http
from basics import render
from basics.odl_http import odl_http_post
import settings
import json

def main():
    if not settings:
        print('Settings must be configured', file=stderr)
    
    render.print_table(odl_http.coordinates)
    print()
    
    config = {"config:module" : [
                        {
                        "type": "lldp-speaker:lldp-speaker",
                        "name": "lldp-speaker",
                        "lldp-speaker:address-destination": "01:23:00:00:00:00",
                        "lldp-speaker:rpc-registry":{
                                                        "name": "binding-rpc-broker",
                                                        "type": "opendaylight-md-sal-binding:binding-rpc-registry"
                                                    },
                        "lldp-speaker:data-broker": {
                                                        "name": "binding-data-broker",
                                                        "type": "opendaylight-md-sal-binding:binding-async-data-broker"
                                                    }
                        }
                        ]
    }
    
    config_str = json.dumps(config)
    try:
        response = odl_http_post(
                      url_suffix='operational/opendaylight-inventory:nodes/node/openflow:1',
                      url_params={},
                      contentType='application/json',
                      content=config_str)
        print(response)
    except Exception as e:
        print(e, file=stderr)


if __name__ == "__main__":
    main()
