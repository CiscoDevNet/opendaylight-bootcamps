<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <flow-name>${flowname}</flow-name>
	<table_id>0</table_id>
    <id>${id}</id>
	<strict>false</strict>
    <installHw>false</installHw>
    <priority>10</priority>    
    <instructions>
        <instruction>
            <order>0</order>
            <go-to-table>
                <table_id>1</table_id>
            </go-to-table>
        </instruction>
    </instructions>
    <match>
    </match>
</flow>