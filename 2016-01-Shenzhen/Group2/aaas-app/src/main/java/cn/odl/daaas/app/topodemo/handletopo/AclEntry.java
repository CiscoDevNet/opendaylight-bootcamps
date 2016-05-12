package cn.odl.daaas.app.topodemo.handletopo;

import org.codehaus.jackson.annotate.JsonProperty;

public class AclEntry 
{
	@JsonProperty("entry-uuid")
	private String uuid;
	
	@JsonProperty("source-network")
	private SourceNetwork srcNetwork;	
	
	
	@JsonProperty("source-port")
	private String srcPort;
	
	@JsonProperty("destination-port")
	private String dstPort;
	
	@JsonProperty("destination-network")
	private DestNetwork dstNetwork;
	
	private String protocol;
	
	private String action;
	
	public SourceNetwork getSrcNetwork() {
		return srcNetwork;
	}

	public void setSrcNetwork(SourceNetwork srcNetwork) {
		this.srcNetwork = srcNetwork;
	}

	public String getSrcPort() {
		return srcPort;
	}

	public void setSrcPort(String srcPort) {
		this.srcPort = srcPort;
	}

	public String getDstPort() {
		return dstPort;
	}

	public void setDstPort(String dstPort) {
		this.dstPort = dstPort;
	}

	public DestNetwork getDstNetwork() {
		return dstNetwork;
	}

	public void setDstNetwork(DestNetwork dstNetwork) {
		this.dstNetwork = dstNetwork;
	}

	public String getProtocol() {
		return protocol;
	}

	public void setProtocol(String protocol) {
		this.protocol = protocol;
	}

	public String getUuid() {
		return uuid;
	}

	public void setUuid(String uuid) {
		this.uuid = uuid;
	}

	public String getAction() {
		return action;
	}

	public void setAction(String action) {
		this.action = action;
	}
		
}
