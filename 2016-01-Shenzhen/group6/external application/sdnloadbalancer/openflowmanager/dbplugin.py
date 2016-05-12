__author__ = 'lijie'
from openflowmanager.models import BackendServer, ClientInfo, VirtualService


def create_backend_server(ip, mac, port):
    """
    Create an instance of BackendServer model and store it into the db
    :param ip:
    :param mac:
    :param port:
    :return:
    """
    bs = BackendServer()
    bs.ipaddr = ip
    bs.macaddr = mac
    bs.ofport = port
    bs.save()


def get_all_backendservers():
    """
    Get all the backend servers
    :return: return a list include dicts  e.g:
        [
            {
                'ipaddr': '1.1.1.1',
                'macaddr': '36:91:5c:4b:50:56',
                'ofport': '5',
                'id': 1
                }
        ]
    """
    servers = []
    for bs in BackendServer.objects.all():
        servers.append({
            'ipaddr': bs.ipaddr,
            'macaddr': bs.macaddr,
            'ofport': bs.ofport,
            'id': bs.id
        })
    return servers


def create_client(ip, mac):
    """
    Create an instance of ClientInfo and store it into the db
    :param ip:
    :param mac:
    :return:
    """
    client = ClientInfo()
    client.ip_addr = ip
    client.mac_addr = mac
    client.save()


def get_all_clients():
    """
    Get all the clients info from db
    :return: an list include several dicts
    """
    clients = []
    for cs in ClientInfo.objects.all():
        clients.append({
            'ipaddr': cs.ip_addr,
            'macaddr': cs.mac_addr,
            'id': cs.id
        })
    return clients


def remove_db_client(client_id):
    cs = ClientInfo.objects.get(id=client_id)
    if cs:
        cs.delete()


def remove_db_backend_server(bs_id):
    bs = BackendServer.objects.get(id=bs_id)
    if bs:
        bs.delete()


def create_db_virtual_service(vip, vport, protocol,  bs_pool):
    """
    Careate an mappping between virtual ip, virtul port and the real server
    :param vip:
    :param vport:
    :param bs_pool: a list ids of the backend servers
    :return:
    """
    virtualservice = VirtualService()
    virtualservice.virtual_ip = vip
    virtualservice.virtual_port = vport
    virtualservice.l4_protocol = protocol
    virtualservice.bs_pool = ','.join(bs_pool)
    virtualservice.save()


def get_all_virtual_services():
    """
    :return: a list include several dicts. e.g:
        [
            {
                'vip': 'xxxxx',
                'vport': '80',
                'protocol': tcp,
                'bs_pool': [1, 2, 3]
                },
                ....,
                ....
            ]
            bs_pool is a list include the ids the db entry of BackendServer in
            the sqlite3 db
    """
    results = []
    virtualsvices = VirtualService.objects.all()
    for vs in virtualsvices:
        results.append({
            'vip': vs.virtual_ip,
            'vport': vs.virtual_port,
            'protocol': vs.l4_protocol,
            'bs_pool': vs.bs_pool.split(','),
            'id': vs.id
        })
    return results


def get_virtual_service_by_vip_and_vport(vip, vport):
    virtual_services = VirtualService.objects.all()

    for vs in virtual_services:
        print  vs.virtual_ip, vs.virtual_port
        print  vip, vport
        if vs.virtual_ip == vip and vs.virtual_port == vport:
            return vs


def get_backend_servser_by_id(bs_id):
    bs = BackendServer.objects.get(id=bs_id)
    return bs


def remove_virtual_service(serid):
    vs = VirtualService.objects.get(id=serid)
    if vs:
        vs.delete()

