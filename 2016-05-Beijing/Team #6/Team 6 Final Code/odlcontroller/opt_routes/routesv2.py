#neighborstate = {router_id1:neighbor_info, router_id2:neighbor_info...}
#neighbor_info = {port_id: [neighbor_id, nexthop]}

neighborstate = {'1.1.1.1':{'2.2.2.2':['192.168.12.2'],'3.3.3.3':['192.168.13.3']},
        '2.2.2.2':{'1.1.1.1':['192.168.12.1'],'4.4.4.4':['192.168.24.4']},
                 '3.3.3.3':{'1.1.1.1':['192.168.13.1'],'4.4.4.4':['192.168.34.4']},
                 '4.4.4.4':{'2.2.2.2':['192.168.24.2'],'3.3.3.3':['192.168.34.3']}}


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
        route['2.2.2.2'][dest1] = [['192.168.25.5'],1]
        route['2.2.2.2'][dest2] = [['192.168.25.5'],1]
    if case == 1:
        route['2.2.2.2'][dest1] = [['null0'],1]
        route['2.2.2.2'][dest2] = [['192.168.25.5'],1]
    if case == 2:
        route['2.2.2.2'][dest1] = [['null0'], 1]
        route['1.1.1.1'][dest2] = [['192.168.15.5'], 1]
    while(True):
        nextroute = updateroute(route, neighborstate)
        if route == nextroute:
            break
        else:
            route = nextroute
    return route

def updateroute(route, neighborstate):
    route_table = route
    for routerid_current in neighborstate:
        for neighbor_id in neighborstate[routerid_current]:
            route_temp = route_table[neighbor_id]
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


#for nn in route_table:
#    kk = convert_route[nn]
#    for bb in route_table[nn]:
#        for cc in bb[0]:
#          d.append([kk,bb,32,cc])


d=[]
convert_route = {'192.18.1.31':'iosxrv-2','192.18.1.30':'iosxrv-1','192.18.1.32':'iosxrv-3','192.18.1.33':'iosxrv-4','192.18.1.34':'iosxrv-5','192.18.1.35':'iosxrv-6','192.18.1.36':'iosxrv-7','192.18.1.37':'iosxrv-8'}
convert_ip = {'iosxrv-2':'192.18.1.31','iosxrv-1':'192.18.1.30','iosxrv-3':'192.18.1.32','iosxrv-4':'192.18.1.33','iosxrv-5':'192.18.1.34','iosxrv-6':'192.18.1.35','iosxrv-7':'192.18.1.36','iosxrv-8':'192.18.1.37'}

#nn=calroute(neighborstate)

mmm=0