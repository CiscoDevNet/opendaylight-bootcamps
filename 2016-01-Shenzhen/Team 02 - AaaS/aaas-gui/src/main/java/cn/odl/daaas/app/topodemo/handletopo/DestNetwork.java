package cn.odl.daaas.app.topodemo.handletopo;

import org.codehaus.jackson.annotate.JsonProperty;

public class DestNetwork {
	@JsonProperty("destination-ip")
	private String destIp;	
	
	@JsonProperty("destination-netmask")
	private String destNetmask;

	public String getDestIp() {
		return destIp;
	}

	public void setDestIp(String destIp) {
		this.destIp = destIp;
	}

	public String getDestNetmask() {
		return destNetmask;
	}

	public void setDestNetmask(String destNetmask) {
		this.destNetmask = destNetmask;
	}
}
