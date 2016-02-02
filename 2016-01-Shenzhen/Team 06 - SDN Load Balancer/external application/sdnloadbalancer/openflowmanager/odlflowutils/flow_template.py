__author__ = 'lijie'
from openflowmanager import constants as con

"""
Templates for odl_http to use to add/del flow on the remote device
"""


InitTemplate = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <priority>2</priority>
    <flow-name>2to1icmp</flow-name>
    <match>
        <in-port>2</in-port>
        <ethernet-match>
            <ethernet-type>
                <type>0x800</type>
            </ethernet-type>
        </ethernet-match>
    </match>
    <id>3</id>
    <table_id>0</table_id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                   <order>0</order>
                   <output-action>
                       <output-node-connector>1</output-node-connector>
                       <max-length>65535</max-length>
                   </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
</flow>
"""


ADD_VIRTUAL_SERVICE_MATCH = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <priority>{priority}</priority>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>0x800</type>
            </ethernet-type>
        </ethernet-match>
        <ipv4-destination>{dst_ipaddress}</ipv4-destination>
                <ip-match>
                    <ip-protocol>6</ip-protocol>,
                    <ip-proto>ipv4</ip-proto>
                </ip-match>
        <{protocol}-destination-port>{dst_port}</{protocol}-destination-port>
            </match>
        <id>{flow_id}</id>
    <table_id>{table_id}</table_id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                   <order>0</order>
                   <output-action>
                            <output-node-connector> CONTROLLER </output-node-connector>
                            <max-length>65535</max-length>
                    </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions></flow>
"""


SERVICE_IN = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <priority>{priority}</priority>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>0x800</type>
            </ethernet-type>
        </ethernet-match>
        <ipv4-destination>{dst_ip}</ipv4-destination>
        <ipv4-source>{src_ip}</ipv4-source>
                <ip-match>
                    <ip-protocol>6</ip-protocol>,
                    <ip-proto>ipv4</ip-proto>
                </ip-match>
                    <tcp-destination-port>{dst_port}</tcp-destination-port>
            </match>
        <id>{flow_id}</id>
    <table_id>{table_id}</table_id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
                         <set-nw-dst-action>
                            <ipv4-address>{bs_ip}</ipv4-address>
                        </set-nw-dst-action>
                        </action>
                                        <action>
                   <order>1</order>
                   <set-dl-dst-action>
                        <address>{bs_mac}</address>
                   </set-dl-dst-action>
                </action>
                <action>
                   <order>2</order>
                   <output-action>
                        <output-node-connector>{bs_port}</output-node-connector>
                       <max-length>65535</max-length>
                   </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>

    <idle-timeout>300</idle-timeout>
    </flow>
"""


SERVICE_OUT = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <priority>{priority}</priority>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>0x800</type>
            </ethernet-type>
        </ethernet-match>
            <ipv4-destination>{dst_ip}</ipv4-destination>
            <ipv4-source>{src_ip}</ipv4-source>
                <ip-match>
                    <ip-protocol>6</ip-protocol>,
                    <ip-proto>ipv4</ip-proto>
                </ip-match>
            </match>
        <id>{flow_id}</id>
    <table_id>{table_id}</table_id>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
                         <set-nw-src-action>
                            <ipv4-address>{vip}</ipv4-address>
                        </set-nw-src-action>
                        </action>
                                        <action>
                   <order>1</order>
                   <set-dl-src-action>
                        <address>{src_mac}</address>
                   </set-dl-src-action>
                </action>
                <action>
                   <order>2</order>
                   <output-action>
                        <output-node-connector>{out_port}</output-node-connector>
                       <max-length>65535</max-length>
                   </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>

    <idle-timeout>300</idle-timeout>
    </flow>
"""

