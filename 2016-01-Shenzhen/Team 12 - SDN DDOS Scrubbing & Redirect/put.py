
from __future__ import print_function

import json
from sys import stderr

from basics import odl_http
from basics import render
from basics.odl_http import odl_http_put
import settings


def main():
    if not settings:
        print('Settings must be configured', file=stderr)
    
    render.print_table(odl_http.coordinates)
    print()
    
    config = {
    "add-flow": {
        "input": {
            "flow-ref": "1",
            "transaction-uri": "1",
            "flow-table": "1",
            "container-name": "1",
            "cookie_mask": "1",
            "buffer_id": "1",
            "out_port": "1",
            "out_group": "1",
            "flags": "CHECK_OVERLAP",
            "flow-name": "1",
            "installHw": "true",
            "barrier": "true",
            "strict": "true",
            "priority": "1",
            "idle-timeout": "1",
            "hard-timeout": "1",
            "cookie": "1",
            "table_id": "1",
            "node": "1"
             }
            }
     }
    
    config_str = json.dumps(config)
    try:
        response = odl_http_put(
                      url_suffix='http://127.0.0.1:8181/restconf/operations/sal-flow:add-flow',
                      url_params={},
                      contentType='application/json',
                      content=config_str)
        print(response)
    except Exception as e:
        print(e, file=stderr)


if __name__ == "__main__":
    main()
