# Service Based Forwarding


---

Slicing the underlay network and assigning priority to different flowspace. 
For example we can divide flowspace (dstip:dstport)=(10.0.0.1:8080) has higher priority 1 
and (10.0.0.1:80) with lower priority 2,which means the traffic in flowspace (10.0.0.1:8080) will pass through paths with high bandwidth.

---

## How to Start


1. Start karaf and install features below

```
feature:install odl-dlux-all odl-restconf odl-l2switch-switch odl-openflowplugin-flow-services-ui
```

2. Start mininet and create topology to connect controller. ***topo.py*** is under poc directory.

```
sudo python topo.py 
```

3. Config service ip and port and specify priority. 0 for low priority and 1 for high.

```
# Set service 10.0.0.4 on port 8080 for high priority.
sudo python netSlice.py -d 10.0.0.4 -p 8080 -r 1

# Set service 10.0.0.3 on port 80 for low priority.
sudo python netSlice.py -d 10.0.0.3 -p 80 -r 0

# You can also use template file fromflow.xml and toflow.xml for config, and use netSlice4template.py
# Make sure script and xml file in same folder.

```



## USAGE:

For test:

```
 python netSlicing.py -d 10.0.0.1 -p 8080 -r 1
 python topo.py
 python clearflow.py
 python netSlicing.py -d 10.0.0.4 -p 8080 -r 1
 python netSlicing.py -d 10.0.0.3 -p 80 -r 0	
 
 mininet>>sudo mn --custom 
 mininet > h4 iperf -s -p 8080 &		 	
 mininet> h2 iperf -c h4 -p 8080 -t 3 -i 1
 mininet > h3 iperf -s -p 80 &		 	
 mininet> h1 iperf -c h3 -p 80 -t 3 -i 1 
```

