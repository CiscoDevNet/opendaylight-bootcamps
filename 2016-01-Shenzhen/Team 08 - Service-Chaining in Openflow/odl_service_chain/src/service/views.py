from django.shortcuts import render
from django.template import loader,Context
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from services.scService import SvcChain


class myView(object):
    def __init__(self, db_str, ctr_ip):
        self.controller_ip = ctr_ip
        self.sc_func = SvcChain(self.controller_ip)
        
    def showNodes(self, request):
        nodes= self.sc_func.get_all_ofnods()
        tem = loader.get_template('scNodes.html')
        header = Context({'nodes':nodes})
        return HttpResponse(tem.render(header))
    
    def showTemplate(self, request):
        sctmps = self.sc_func.get_all_templates()
        tem = loader.get_template('scTem.html')
        header = Context({'sctmps':sctmps})
        return HttpResponse(tem.render(header));
    
    def showInstance(self, request):
        scInss = self.sc_func.get_all_instances()
        tem = loader.get_template('scIns.html')
        header = Context({'scInss':scInss})
        return HttpResponse(tem.render(header))
    
    def showBinding(self, request):
        binds = self.sc_func.get_all_apps()
        tem = loader.get_template('scBind.html')
        header = Context({'binds':binds})
        return HttpResponse(tem.render(header));
    
    @csrf_exempt
    def addtemplate(self, request):
        tplt_id = request.POST['id']
        tplt_name = request.POST['name']
        tplt_pipe = request.POST['pipe']
        tplt = self.sc_func.define_sc_tplt(pipeline=tplt_pipe, tpltName=tplt_name,tpltID=tplt_id)
        return HttpResponseRedirect('/showtemp')
    
    @csrf_exempt
    def addins(self, request):
        inst_id = request.POST['scInsID']
        tplt_id = request.POST['scTemID']
        inst_proto = request.POST['protocol']
        inst_port = request.POST['port']
        inst = self.sc_func.define_sc_inst(tplt_id, inst_proto, inst_port,inst_id)
        return HttpResponseRedirect('/showins')
    
    @csrf_exempt
    def addbind(self, request):
        node_id = request.POST['NodeID']
        inst_id = request.POST['scID']
        self.sc_func.define_sc_app_by_id(node_id, inst_id)
        return HttpResponseRedirect('/showbind')
    
    @csrf_exempt
    def updateType(self, request):
        id = request.POST['NodeID']
        type = request.POST['type']
        print id, type
        self.sc_func.update_node_type(id,type)
        
        return HttpResponseRedirect('/shownodes')
       
def showNodes(request):
    
    nodes = NodeTable.objects.all()
    tem = loader.get_template('scNodes.html')
    header = Context({'nodes':nodes})
    return HttpResponse(tem.render(header));

def showTemplate(request):
    sctmps = scTemplate.objects.all()
    tem = loader.get_template('scTem.html')
    header = Context({'sctmps':sctmps})
    return HttpResponse(tem.render(header));

def showInstance(request):
    scInss = scInstance.objects.all()
    tem = loader.get_template('scIns.html')
    header = Context({'scInss':scInss})
    return HttpResponse(tem.render(header));

def showBinding(request):
    binds = scBinding.objects.all()
    tem = loader.get_template('scBind.html')
    header = Context({'binds':binds})
    return HttpResponse(tem.render(header));

@csrf_exempt
def addtemplate(request):
    id = request.POST['id']
    print(request.POST['name'])
    print(request.POST['pipe'])
    return HttpResponseRedirect('/showtemp')

@csrf_exempt
def addins(request):
    print(request.POST['scInsID'])
    print(request.POST['scTemname'])
    print(request.POST['protocol'])
    print(request.POST['port'])
    return HttpResponseRedirect('/showins')

@csrf_exempt
def addbind(request):
    print(request.POST['NodeID'])
    print(request.POST['scID'])
    return HttpResponseRedirect('/showbind')

# Create your views here.
