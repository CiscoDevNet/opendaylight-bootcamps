Our original ideas:
  Limit traffic flood to specific destination. For example, on the Alibaba¡¯s shopping day of 11th Nov, a flood of traffic would break down servers and waste precious bandwidth.

  To solve this, our first idea is using randomly drop some packets or limit rate. We think these mothods can low down the server's load and Clients will still have a chance to connect to server and get service.

Problems:
    Firstly, QoS yang and Flow Spec are not supported by XRV right now. Secoundly, It is hard to generate packerts flood in dcloud. 

Decision :
    ACL yang is support but not fit to our idea. So why not open ACL setting as a Service?
    ACL is useful. It provides a basic level of security for the network offers flow control for network traffic. But Configuration is painful.
There are lots of network devices and configration is error-prone.

Project:
    AaaS: ACL as a service 
    
    Our project provides ACL as a Service. We offers Restful API: One API, everyting set. 

Our potential customers:
    Network operator
    Internet Company
    ODL Bootcamp^_^ 
    
    
Architecture:
    we embody an internal app based on ODL, which tries to facilitate the configuration and management of ACL,with what we learned in the ODL bootcamp.Also We Use Cisco's cisco next ui framwork to operate the network and show our works.

    For the internal app, it realizes ACL configuration on all the router we needed and provide APIs for advanced users. Besides, we use Cisco Next UI to show how to configure the ACL

