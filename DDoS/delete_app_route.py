#!/usr/bin/env python
from router_attributes import attributes
from v4_uni_app_route import app_route

attrib = attributes()
route = app_route("localhost")

#attrib.set_communities("100:100")
attrib.set_next_hop("192.0.2.1")

print attrib

route.del_app_route("45.0.0.27/32")
