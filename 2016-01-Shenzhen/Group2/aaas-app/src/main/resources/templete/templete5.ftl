<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <flow-name>${flowname}</flow-name>
    <table_id>1</table_id>
    <id>${id}</id>
    <installHw>false</installHw>
    <strict>false</strict>
	
    <priority>100</priority>
	
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
                    <drop-action/>
                </action>
            </apply-actions>
        </instruction>
    </instructions>
    <match>
    </match>
</flow>