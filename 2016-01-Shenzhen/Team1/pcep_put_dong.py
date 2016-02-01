from basics.odl_http import odl_http_post
import settings

def pcep_update_lsp():
    request_content = {
        "input" : {
            "node" : "pcc://27.27.27.27",
            "name" : "FC2DC",
            "network-topology-ref": "/network-topology:network-topology/network-topology:topology[network-topology:topology-id=\"pcep-topology\"]",
            "arguments": {
                "pcep-ietf-stateful:lsp": {
                    "administrative": "true",
                    "delegate": "true"
                },
                "ero" : {
                    "subobject" : [
                        {
                            "loose" : "false",
                            "ip-prefix" : { "ip-prefix" : "48.0.0.22/32" }
                        },
                        {
                            "loose" : "false",
                            "ip-prefix" : { "ip-prefix" : "49.0.0.30/32" }
                        },
                        {
                            "loose" : "false",
                            "ip-prefix" : { "ip-prefix" : "56.0.0.29/32" }
                        },
                                            {
                            "loose" : "false",
                            "ip-prefix" : { "ip-prefix" : "1.2.3.4/32" }
                        }
                    ]
                }
            }
        }
    }
        
    
    response = odl_http_post(
        url_suffix = "operations/network-topology-pcep:update-lsp",
        url_params={},
        contentType = "application/json",
        content = request_content,
        accept='application/json',
        expected_status_code = 200
        )
    print response