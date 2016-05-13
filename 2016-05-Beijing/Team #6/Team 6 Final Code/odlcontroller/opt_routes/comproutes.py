#neighborstate = {router_id1:neighbor_info, router_id2:neighbor_info...}
#neighbor_info = {port_id: [neighbor_id, nexthop]}
from createroutes import test_route_create

neighborstate = {'198.18.1.30':{'198.18.1.34':['45.0.0.27'],'198.18.1.31':['58.0.0.22'],'198.18.1.32':['44.0.0.24']},
        '198.18.1.31':{'198.18.1.30':['58.0.0.22'],'198.18.1.34':['48.0.0.27'],'198.18.1.37':['49.0.0.30']},
        '198.18.1.32':{'198.18.1.30':['44.0.0.21'],'198.18.1.35':['51.0.0.28'],'198.18.1.37':['57.0.0.30']},
        '198.18.1.33':{'198.18.1.35':['53.0.0.28'],'198.18.1.36':['54.0.0.29']},
        '198.18.1.34':{'198.18.1.30':['45.0.0.21'],'198.18.1.31':['48.0.0.22']},
        '198.18.1.35':{'198.18.1.32':['51.0.0.24'],'198.18.1.33':['53.0.0.26']},
        '198.18.1.36':{'198.18.1.37':['56.0.0.30'],'198.18.1.33':['54.0.0.26'],},
        '198.18.1.37':{'198.18.1.31':['49.0.0.22'],'198.18.1.32':['57.0.0.24'],'198.18.1.36':['56.0.0.29']}}



def calroute(case=1,neighborstate=neighborstate):
    route = {}
    dest1 = '55.55.55.55'
    dest2 = '66.66.66.66'
    #init route_table
    for routerid_current in neighborstate:
        route[routerid_current] = {}
        for neighbor_id in neighborstate[routerid_current]:
            route[routerid_current][neighbor_id] = [neighborstate[routerid_current][neighbor_id],1]
    if case == 0:
        route['198.18.1.31'][dest1] = [['48.0.0.27'],1]
        route['198.18.1.31'][dest2] = [['48.0.0.27'],1]
    if case == 1:
        route['198.18.1.31'][dest1] = [['192.0.2.1'],1]
        route['198.18.1.31'][dest2] = [['48.0.0.27'],1]
    if case == 2:
        route['198.18.1.31'][dest1] = [['192.0.2.1'], 1]
        route['198.18.1.30'][dest2] = [['45.0.0.27'], 1]
    p = len(route)
    while(p > 0):
        route = dict(updateroute(route, neighborstate))
        p = p - 1
    return route

def updateroute(route, neighborstate):
    route_table = dict(route)
    for routerid_current in neighborstate:
        for neighbor_id in neighborstate[routerid_current]:
            route_temp = dict(route_table[neighbor_id])
            if routerid_current in route_temp:
                route_temp.pop(routerid_current)
            k = {}
            for temp in route_temp:
                k[temp] = []
                k[temp].append([neighbor_id])
                k[temp].append(route_temp[temp][1])
                k[temp][1] =  k[temp][1] + 1
                if temp not in route_table[routerid_current]:
                    route_table[routerid_current].update(k)
                if temp in route_table[routerid_current] and route_table[routerid_current][temp][1] > k[temp][1]:
                    route_table[routerid_current].update(k)
                if temp in route_table[routerid_current] and route_table[routerid_current][temp][1] == k[temp][1]:
                    [c] = k[temp][0]
                    if c not in route_table[routerid_current][temp][0]:
                        route_table[routerid_current][temp][0] = k[temp][0] + route_table[routerid_current][temp][0]
                k.pop(temp)
    return route_table





convert_route = {'198.18.1.31':'iosxrv-2','198.18.1.30':'iosxrv-1','198.18.1.32':'iosxrv-3','198.18.1.33':'iosxrv-4','198.18.1.34':'iosxrv-5','198.18.1.35':'iosxrv-6','198.18.1.36':'iosxrv-7','198.18.1.37':'iosxrv-8'}
convert_ip = {'iosxrv-2':'192.18.1.31','iosxrv-1':'192.18.1.30','iosxrv-3':'192.18.1.32','iosxrv-4':'192.18.1.33','iosxrv-5':'192.18.1.34','iosxrv-6':'192.18.1.35','iosxrv-7':'192.18.1.36','iosxrv-8':'192.18.1.37'}
static_route=[]

def main():
    nn=calroute(1,neighborstate)
    for tt in nn:
        kk = convert_route[tt]
        for bb in nn[tt]:
            for cc in nn[tt][bb][0]:
                static_route.append([kk,bb,32,cc])
    test_route_create(static_route)


main()
