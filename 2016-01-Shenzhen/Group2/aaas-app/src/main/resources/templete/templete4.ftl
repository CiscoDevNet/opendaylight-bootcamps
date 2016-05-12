<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <flow-name>${flowname}</flow-name>
    <table_id>1</table_id>
    <id>${id}</id>
    <installHw>false</installHw>
    <strict>false</strict>
    
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
                    <output-action>
                        <output-node-connector>${actionOutput}</output-node-connector>
                    </output-action>
                </action>
            </apply-actions>
        </instruction>
    </instructions>

    <match>
        <ethernet-match>
            <ethernet-type>
                <type>2054</type>
            </ethernet-type>
        </ethernet-match>        
        <arp-target-transport-address>${destIp}</arp-target-transport-address>
        <tunnel>
            <tunnel-id>${tunnelId}</tunnel-id>
        </tunnel>
    </match>
</flow>