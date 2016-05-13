from django.shortcuts import render
from django.http import HttpResponse
from models import AppInfo, Nodes, LinkNodes
from opt_routes.cdp_get_topo import *
from opt_routes.comproutes import *
import json


DictNodes = {
           'iosxrv-1':1,
           'iosxrv-2':2,
           'iosxrv-3':3,
           'iosxrv-4':4,
           'iosxrv-5':5,
           'iosxrv-6':6,
           'iosxrv-7':7,
           'iosxrv-8':8,
    }

def changeState(request):
    action = request.GET['action']
    if action == '1':
        calroute(0)
        AppInfo.objects.all().filter(id=1).update(action='1', health='Good')
        AppInfo.objects.all().filter(id=2).update(action='1', health='Good')
        return HttpResponse("All status all right now.")
    elif action == '2':
        calroute(1)
        AppInfo.objects.all().filter(id=1).update(action='2')
        AppInfo.objects.all().filter(id=2).update(action='2')
        return HttpResponse("iosxrv-2 is down")
    else :
        calroute(2)
        AppInfo.objects.all().filter(id=1).update(action='3', health='Bad')
        AppInfo.objects.all().filter(id=2).update(action='3')
        
        return HttpResponse("iosxrv-8 to iosxrv-2 has latency")


def updateLink():
    linkinfo = link_info()
    print(linkinfo)
    #linkinfo = {
    #         1: ('iosxrv-8', 'iosxrv-3'),
    #         2: ('iosxrv-8', 'iosxrv-1'), 
    #         3: ('iosxrv-8', 'iosxrv-2'), 
    #         4: ('iosxrv-8', 'iosxrv-6'), 
    #         5: ('iosxrv-8', 'iosxrv-7'), 
    #        6: ('iosxrv-7', 'iosxrv-4'), 
    #         7: ('iosxrv-6', 'iosxrv-3'), 
    #         8: ('iosxrv-6', 'iosxrv-4'), 
    #         9: ('iosxrv-5', 'iosxrv-1'), 
    #         10: ('iosxrv-5', 'iosxrv-2'), 
    #         11: ('iosxrv-3', 'iosxrv-1')
    #}
    for linkinf in linkinfo:
        print(DictNodes[linkinfo[linkinf][1]])
        p = LinkNodes(sourceN=DictNodes[linkinfo[linkinf][0]],targetN=DictNodes[linkinfo[linkinf][1]], nameL='link',statusL=1)
        p.save()
    


def add(request):
    updateLink()
    nodes = Nodes.objects.all()
    linknodes = LinkNodes.objects.all()
    topologyData = {"nodes":[],"links":[]}
    for node in nodes:
        topologyData["nodes"].append({"id": node.id, "x": node.xpos, "y": node.ypos, "name": node.name})
    for linknode in linknodes:
        topologyData["links"].append({"id": linknode.id, "source": linknode.sourceN, "target": linknode.targetN,})
        linknode.delete()
    print(topologyData)
    return HttpResponse(json.dumps(topologyData),content_type="application/json")

def addroutes(request):
    appid = request.GET['id']
    topologyData = {
    "nodes": [
            {"id": 0, "x": 150, "y": 300, "name": "por"},
            {"id": 1, "x": 350, "y": 300, "name": "sfc"},
            {"id": 2, "x": 300, "y": 175, "name": "sea"},
            {"id": 3, "x": 500, "y": 175, "name": "sjc"},
            {"id": 4, "x": 450, "y": 50, "name": "min"},
            {"id": 5, "x": 700, "y": 175, "name": "lax"},
            {"id": 6, "x": 650, "y": 50, "name": "kcy"},
            {"id": 7, "x": 850, "y": 100, "name": "san"},
        ],
        "links": [
            {"source": 0, "target": 1, "id": 0},
            {"source": 0, "target": 2, "id": 1},
            {"source": 1, "target": 3, "id": 2},
            {"source": 2, "target": 4, "id": 3},
            {"source": 3, "target": 4, "id": 4},
            {"source": 4, "target": 6, "id": 5},
            {"source": 3, "target": 5, "id": 6},
            {"source": 5, "target": 6, "id": 7},
            {"source": 5, "target": 7, "id": 8},
            {"source": 6, "target": 7, "id": 9}
        ]
    };
    return HttpResponse(json.dumps(topologyData),content_type="application/json")



def add2(request):
    topologyData = {
    "nodes": [
            {"id": 0, "x": 150, "y": 300, "name": "por"},
            {"id": 1, "x": 350, "y": 300, "name": "sfc"},
            {"id": 2, "x": 300, "y": 175, "name": "sea"},
            {"id": 3, "x": 500, "y": 175, "name": "sjc"},
            {"id": 4, "x": 450, "y": 50, "name": "min"},
        ],
        "links": [
            {"source": 0, "target": 1, "id": 0},
            {"source": 0, "target": 2, "id": 1},
            {"source": 1, "target": 3, "id": 2},
            {"source": 2, "target": 3, "id": 3},
            {"source": 2, "target": 4, "id": 4},
            {"source": 3, "target": 4, "id": 5},
        ]
    };
    return HttpResponse(json.dumps(topologyData),content_type="application/json")

def index(request):
    return render(request, 'index.html')

def applist(request):
    list = AppInfo.objects.all()
    return render(request, 'applist.html', {'list': list})

def appdetail(request):
    appid = request.GET['id']
    appinfo = AppInfo.objects.get(id=appid)
    return render(request, 'appdetail.html', {'appinfo': appinfo, 'appid':appid})

def test(request):
    return render(request, 'test.html')