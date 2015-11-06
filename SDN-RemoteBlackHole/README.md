#SDN-Programatic Flow Management
###############################

Team Members: Oleg Berzin, Michael Kowal, Yueping Zhang, Kevin Boutarel

## Goal of the Project  

Demonstrating ODL capabilities for programatic control of flows in the network using BGP flowspec or BGP v4.


## How to Use this Application  

Setup the Loc RIB with the IP address of the ODL controller (in our case `localhost`):  
	python put-bgp-rib.py 127.0.0.1

Setup the App RIB and the connection to the Loc RIB with 1) the IP address of the ODL controller and 2) the ID of the Loc RIB (IP address of the Controller):  
	python put-app-rib.py 127.0.0.1 127.0.0.1

Setup the BGP Peer with the router with 1) the IP address of the ODL controller and 2) the IP address of the router:  
	python put-bgp-peer.py 127.0.0.1 198.18.1.30

Setup the BGP Neighbor between the router and NETCONF witht the IP address of the ODL controller:  
	python put-bgp-neighbor.py 127.0.0.1

However, the script returned a `400` or `500` return code so we were unable to set it up automatically.  

Another alternative is to connect manually to the router and set up the neighbor from there.  
The following commands were used:  
	ssh cisco@198.18.1.30
	conf t
	router bgp 65504
	neighbor MY_IP_ADDRESS
	remote-as 65504
	update-source MgmtEth0/0/CPU0/0
	address-family ipv4 unicast
	route-reflector-client
	commit
	end  

Everything is setup architecturaly for the scripts to run.  

To monitor the traffic on the interface, simply run:  
	python monitor.py

This will run continuously by getting the bytes sent to the client and finding the difference with the previous run.  
The bytes are taken every 2 seconds.  
If the difference hits the threshold MAX_OCCURENCES times, a trigger will be done to insert a route (with `insert_route.py`) to the controller which will stop the connection to the client.  
If the route is set, the script will monitor the number of times a normal behavior is happening on the connection.  
After MAX_NORMAL runs, the script will trigger `delete_route.py` which will delete the route that we created previously.  
This process is repeated infinitely.  


## Future Goals

This implementation ueses ipv4 unicast routes.  
The original plan was to use flowspec but a bug on the router failed to accept flowspec routes due to community bugs.  
When that bug is fixed, the scripts `insert_route.py` and `delete_route.py` should be modified to insert and delete flowspec routes, respectively.  

Another enhancement would be to have a broader monitoring with a more network wide view.
With this implementation, we currently know where the Ddos attack is coming from.
It would be better to have the script monitor multiple routers, with known topologies, and surveys the various interfaces.  