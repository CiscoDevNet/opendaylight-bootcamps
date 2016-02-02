__author__ = 'lijie'
import dbplugin
import json


def make_flow_cmd(cmds):
    pass


def get_bs_pool():
    """
    Get all the backend servers
    :return: a list include several dicts. e.g:
        [
            {
                'ipaddr': '100.100.100.100',
                'bs_id': 'xxx',
            },
            ....
        ]
    ipaddr: ip address of the backend server
    bs_id: the id of bs db entry in the sqlite3
    """
    bs_pool = []
    bservers = dbplugin.get_all_backendservers()
    for bs in bservers:
        bs_pool.append({
            'ipaddr': bs.get('ipaddr'),
            'bs_id': bs.get('id')
        })
    return bs_pool


def get_json_from_str(str_data):
    return json.loads(str_data)


