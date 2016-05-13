from django.shortcuts import render
from django.http import HttpResponse
import requests

bind_host = '192.168.255.134'
# Create your views here.
def index(request):
    tr1, tr2 = refresh_req()
    reset_req()

    return render(request, 'index.html', {'TTT': str(tr1) + 'kbps', 'BBB': str(tr2) + 'kbps', 'SSS': 'yes'})


def refresh(request):
    tr1, tr2 = refresh_req()

    return HttpResponse('{"TTT": "' + str(tr1) + 'kbps", "BBB": "' + str(tr2) + 'kbps"}')


def switch(request):
    switch_req()
    return HttpResponse('OK')


def reset(request):
    return HttpResponse('OK')


def refresh_req():
    url = "http://" + bind_host + ":8181/restconf/operational/network-topology:network-topology/topology/topology-netconf/node/iosxrv-8/yang-ext:mount/Cisco-IOS-XR-pfi-im-cmd-oper:interfaces"

    headers = {
        'authorization': "Basic YWRtaW46YWRtaW4=",
        'cache-control': "no-cache",
        'postman-token': "a16e3eab-fcea-a361-47ae-ca89f84bd71b"
        }

    response = requests.request("GET", url, headers=headers)
    string = response.text
    string = string.replace('false', 'False').replace('true', 'True')
    res = eval(string)
    if 'interfaces' in res.keys():
        tr1 =  res['interfaces']['interface-xr']['interface'][1]['data-rates']['output-data-rate']
        tr2 =  res['interfaces']['interface-xr']['interface'][2]['data-rates']['output-data-rate']
    else:
        tr1 = 0
        tr2 = 0

    return tr1, tr2


def switch_req():
    url = "http://" + bind_host + ":8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/iosxrv-8/yang-ext:mount/Cisco-IOS-XR-ipv4-acl-cfg:ipv4-acl-and-prefix-list/accesses/access/penxiao"

    payload = "{\n    \"access\": [\n    {\n        \"access-list-name\": \"penxiao\",\n        \"access-list-entries\": {\n          \"access-list-entry\": [\n            {\n              \"sequence-number\": 20,\n              \"grant\": \"permit\"\n            },\n            {\n              \"sequence-number\": 10,\n              \"grant\": \"permit\",\n              \"dscp\": \"cs1\",\n              \"next-hop\": {\n                \"next-hop-type\": \"regular-next-hop\",\n                \"next-hop-1\": {\n                  \"next-hop\": \"49.0.0.22\"\n                }\n              }\n            }\n          ]\n        }\n      }\n    ]\n}"
    headers = {
        'authorization': "Basic YWRtaW46YWRtaW4=",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "71f8b41a-ea7e-7c82-1070-f65ea165155b"
        }

    response = requests.request("PUT", url, data=payload, headers=headers)

    print(response.text)

    url = "http://" + bind_host + ":8181/restconf/config/opendaylight-inventory:nodes/node/iosxrv-8/yang-ext:mount/Cisco-IOS-XR-ifmgr-cfg:interface-configurations/interface-configuration/act/GigabitEthernet0%252F0%252F0%252F4"

    payload = "{\n  \"interface-configuration\": [\n    {\n      \"active\": \"act\",\n      \"interface-name\": \"GigabitEthernet0/0/0/4\",\n      \"Cisco-IOS-XR-ip-pfilter-cfg:ipv4-packet-filter\": {\n        \"inbound\": {\n          \"name\": \"penxiao\"\n        }\n      },\n      \"Cisco-IOS-XR-drivers-media-eth-cfg:ethernet\": {\n        \"speed\": \"10\"\n      },\n      \"Cisco-IOS-XR-ipv4-io-cfg:ipv4-network\": {\n        \"addresses\": {\n          \"primary\": {\n            \"netmask\": \"255.255.255.0\",\n            \"address\": \"56.0.0.30\"\n          }\n        }\n      }\n    }\n  ]\n}"
    headers = {
        'content-type': "application/json",
        'authorization': "Basic YWRtaW46YWRtaW4=",
        'cache-control': "no-cache",
        'postman-token': "2cadba9d-18dd-e0fd-95d2-604c86cf78d6"
        }

    response = requests.request("PUT", url, data=payload, headers=headers)

    print(response.text)


def reset_req():
    pass