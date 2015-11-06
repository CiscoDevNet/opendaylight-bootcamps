import json 
import requests
import pprint

base_hdr = {	'Authorization' : 'Basic YWRtaW46YWRtaW4=',
					'Content-Type' : 'application/json' }
get_url = "http://localhost:8181/restconf/operational/bgp-rib:bgp-rib/rib/example-bgp-rib"
put_url = "http://localhost:8181/restconf/config/bgp-rib:application-rib/example-app-rib/tables/bgp-types:ipv4-address-family/bgp-types:unicast-subsequent-address-family/ipv4-routes/"
sample_prefixes_dict = {}

# read rib
def get_rib():
    resp = requests.get(get_url, headers=base_hdr)
    json_str = resp.text    
    jd = json.loads(json_str)
    return jd

# add communities to rib from file
def get_rib_with_communities(jd):
    indiv_routes = []
    ribs = jd["rib"]
    for rib in ribs:
        tables = rib["loc-rib"]["tables"]
        for table in tables:
            if "bgp-inet:ipv4-routes" in table:
                routes = table["bgp-inet:ipv4-routes"]["ipv4-route"]
                for route in routes:
                    prefix = route["prefix"]
		    attributes_dict = route["attributes"]
        	    if prefix in sample_prefixes_dict:
            	        attributes_dict['communities'] = [{"as-number": int(c.split(":")[0]), \
                                               "semantics": c.split(":")[1]} \
                                              for c in sample_prefixes_dict[prefix].split()]
		    indiv_routes.append(route)
    route_dict = {}
    route_dict['bgp-inet:ipv4-route'] = indiv_routes
    return route_dict

#put rib with new communities added
def put_rib(new_rib):
    json_rib = json.dumps(new_rib)
    resp = requests.put(put_url, data=json_rib, headers=base_hdr)
    print resp.text

# read file with list of prefixes and communities
def init_prefixes_dict(filename):
    for line in open(filename, 'r'):
        elements = line.split(',')
        if len(elements) > 1:
            comms = ' '.join(elements[1:])  
            sample_prefixes_dict[elements[0]] = comms
        

init_prefixes_dict("TestCommunitiesFile.txt")
old_rib = get_rib()
new_rib = get_rib_with_communities(old_rib)
put_rib(new_rib)

