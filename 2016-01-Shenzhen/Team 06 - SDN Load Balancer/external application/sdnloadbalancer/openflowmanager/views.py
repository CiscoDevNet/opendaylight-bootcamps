import random
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from openflowmanager import utils
from openflowmanager import dbplugin
from openflowmanager import constants as con
from openflowmanager.odlflowutils import odl_http
import pdb


def index(request):
    # Index view of the external application for odl controller
    return render_to_response('app.html')


@csrf_exempt
def add_virtual_service(request):
    vip = request.POST.get(con.VIP)
    vport = request.POST.get(con.VPORT)
    bs_pool = request.POST.getlist('checkbox')
    protocol = request.POST.get(con.PRO)
    if vip and vport and bs_pool:
        dbplugin.create_db_virtual_service(vip, vport, protocol, bs_pool)
        # add flow match the vip and vport to send to the controller
        odl_http.add_virtual_service_flow(vip, vport, protocol)

    # data to list for user to chose
    list_bs_pool = utils.get_bs_pool()
    virtual_services = dbplugin.get_all_virtual_services()
    print virtual_services
    return render_to_response('addservice.html', {
        "bs_pool": bs_pool,
        "virtual_services": virtual_services,
        "list_bs_pool": list_bs_pool})


@csrf_exempt
def add_backend_servers(request):
    # get the ip and mac address from the request, if ip and mac are None, then
    # just display the list the backend servers, else add the ip and mac into
    # to db
    ip_addr = request.POST.get(con.IP_ADDR)
    mac_addr = request.POST.get(con.MAC)
    ofport = request.POST.get(con.OFPORT)

    if ip_addr and mac_addr and ofport:
        dbplugin.create_backend_server(ip_addr, mac_addr, ofport)

    # Get all the exist items
    backends = dbplugin.get_all_backendservers()
    return render_to_response('backends.html', {"backends": backends})


def del_backend_servers(request, serverid):
    # delete an backend server due to the servierid
    dbplugin.remove_db_backend_server(serverid)
    return HttpResponseRedirect("/backends")


@csrf_exempt
def add_clients(request):
    ip_addr = request.POST.get(con.IP_ADDR)
    mac_addr = request.POST.get(con.MAC)

    if ip_addr and mac_addr:
        dbplugin.create_client(ip_addr, mac_addr)

    clients = dbplugin.get_all_clients()
    return render_to_response('clients.html', {'clients': clients})


def del_client(request, clientid):
    dbplugin.remove_db_client(clientid)
    return HttpResponseRedirect('/clients')


@csrf_exempt
def packetin(request):
    """
     Deal with the information sent from odl controller
    :param request:
    :return:
    """
    # pdb.set_trace()
    info = request.body.split(',')
    print info
    # # TODO add flow on the device
    dst_ip = info[3]
    dst_port = info[5]
    client_ip = info[1]
    vser = dbplugin.get_virtual_service_by_vip_and_vport(dst_ip, dst_port)
    print "vser", vser
    bs_pool = []
    if vser:
        # TODO add loadbalance flow
        backend_servers = vser.bs_pool.split(',')
        # Get all the bs ip from the sqlite3
        for bs_id in backend_servers:
            bs = dbplugin.get_backend_servser_by_id(bs_id)
            bs_pool.append(bs)
    else:
        return HttpResponse("failed")
    if bs_pool:
        # TODO choose a ip from the bs_pool and add flow
        pass
        chosen_bs = random.choice(bs_pool)
        odl_http.add_service_in_flow(vser.virtual_ip, vser.virtual_port,
                                     chosen_bs.ipaddr, chosen_bs.macaddr,
                                     chosen_bs.ofport, client_ip)
        odl_http.add_service_out_flow(vser.virtual_ip, chosen_bs.ipaddr,
                                      client_ip)
    return HttpResponse("success")


def delvirtualservice(rquest, serid):
    dbplugin.remove_virtual_service(serid)
    return HttpResponseRedirect('/addservice')