import json

import requests
from requests.auth import HTTPBasicAuth
from flask import current_app


def get_topology():
    def __get_node_id_by_text(nodes, text):
        for node in nodes:
            if node['node_id'] == text:
                return node['id']

    def __get_topology_node_label(node):
        if node['node-id'].find('host') != -1:
            return 'host %s(%s)' % (node['host-tracker-service:addresses'][0]['ip'], node['host-tracker-service:id'])
        node_id_name_mapping = {'openflow:1': 'VDC1 Swtich', 'openflow:2': 'VDC2 Swtich', 'openflow:3': 'Access Switch'}
        return node['node-id'] if node_id_name_mapping.get(node['node-id']) is None else '%s(%s)' % (
            node_id_name_mapping[
                node['node-id']], node['node-id'])

    resp = requests.get(
        '%s/operational/network-topology:network-topology' % current_app.config['ODL_ENDPOINT'],
        auth=HTTPBasicAuth(current_app.config['ODL_USER'],
                           current_app.config['ODL_PWD']),
        headers={'Accept': 'application/json, text/plain, */*'})
    nodes = []
    links = []

    if resp.status_code == 200:
        full_topology = resp.json()
        for item in full_topology['network-topology']['topology']:
            if item.get('node'):
                for node in item.get('node'):
                    nodes.append({'id': str(len(nodes) + 1),
                                  'label': __get_topology_node_label(node),
                                  'node_id': node['node-id'],
                                  'group': 'swtich' if node['node-id'].find('host') == -1 else 'host',
                                  'title': 'Name: <b>' + node['node-id'] + '</b><br>Type: Switch',
                                  'rawData': node})
            if item.get('link'):
                for link in item.get('link'):
                    src_port = __get_node_id_by_text(nodes, link['source']['source-node'])
                    dest_port = __get_node_id_by_text(nodes, link['destination']['dest-node'])
                    links.append({
                        'id': str(len(links) + 1),
                        'source': str(src_port),
                        'target': str(dest_port),
                        'title': 'Source Port: <b>' + link['source']['source-tp'] + '</b><br>Dest Port: <b>' +
                                 link['destination']['dest-tp'] + '</b>',
                        'rawData': link
                    })

    return {'nodes': nodes, 'links': links}


def del_open_flow(of_sw, flow_id):
    send_json = {'id': flow_id}
    resp = requests.delete('%s/config/opendaylight-inventory:nodes/node/%s/table/%s/flow/%s' %
                           (current_app.config['ODL_ENDPOINT'], of_sw, 0, flow_id),
                           data=send_json,
                           auth=HTTPBasicAuth(current_app.config['ODL_USER'],
                                              current_app.config['ODL_PWD']),
                           headers={'Accept': 'application/json, text/plain, */*',
                                    'Content-Type': 'application/json;charset=UTF-8'})
    return resp.status_code == 200


def add_open_flow(of_sw, flow):
    flow_json = json.dumps({'flow': [flow]})
    resp = requests.put('%s/config/opendaylight-inventory:nodes/node/%s/table/%s/flow/%s' %
                        (current_app.config['ODL_ENDPOINT'], of_sw, flow['table_id'], flow['id']),
                        flow_json,
                        auth=HTTPBasicAuth(current_app.config['ODL_USER'],
                                           current_app.config['ODL_PWD']),
                        headers={'Accept': 'application/json, text/plain, */*',
                                 'Content-Type': 'application/json;charset=UTF-8'})
    return resp.status_code == 200


def simple_add_open_flow(access_sw, flow_id, in_port, out_port, add_ctrl=True):
    actions = [{
        "order": 0,
        "apply-actions": {
            "action": []
        }}]
    ctrl_order = 0
    if isinstance(out_port, (list, tuple)):
        for idx, o in enumerate(out_port):
            actions[0]['apply-actions']['action'] \
                .append({"order": idx, "output-action": {"output-node-connector": o, "max-length": "65535"}})
            ctrl_order = idx
    else:
        actions[0]['apply-actions']['action'] \
            .append({"order": 0, "output-action": {"output-node-connector": out_port, "max-length": "65535"}})

    if add_ctrl:
        actions[0]['apply-actions']['action'].append({
            "order": ctrl_order + 1,
            "output-action": {"output-node-connector": "CONTROLLER", "max-length": "65535"}
        })
    flow = {'hard-timeout': 0, 'idle-timeout': 0, 'installHw': False, 'strict': False, 'table_id': '0',
            'id': flow_id, 'priority': 2, 'match': {'in-port': '%s:%s' % (access_sw, in_port)},
            'instructions': {'instruction': actions}}
    add_open_flow(access_sw, flow)
