'''
Created on Jan 22, 2016

@author: chuck
'''
import httplib2
def clearflow():
    for i in range(8):
        h = httplib2.Http(".cache")
        h.add_credentials('admin', 'admin')
        resp, content = h.request(
          uri = 'http://10.1.0.242:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(i+1)+'/table/0/',
          method = 'DELETE',
          headers={'Content-Type' : 'application/xml'}
          )
    return resp, content

if __name__=="__main__":
    clearflow()