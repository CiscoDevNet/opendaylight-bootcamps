<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<flow xmlns="urn:opendaylight:flow:inventory">
    <flow-name>${flowname}</flow-name>
    <table_id>0</table_id>
    <id>${id}</id>
    <installHw>false</installHw>
    <strict>false</strict>
	<priority>10</priority>
    <instructions>
        <instruction>
            <order>0</order>
            <apply-actions>
                <action>
                    <order>0</order>
					<set-field>
						<tunnel>
							<tunnel-id>${tunnelId}</tunnel-id>
						</tunnel>
					</set-field>
                </action>
            </apply-actions>
        </instruction>
        <instruction>
            <order>1</order>
            <go-to-table>
                <table_id>1</table_id>
            </go-to-table>
        </instruction>
    </instructions>

    <match>
        <in-port>${matchInPort}</in-port>
    </match>
</flow>