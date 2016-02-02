package cn.odl.daaas.app.topodemo.handletopo;

import org.codehaus.jackson.annotate.JsonProperty;

public class SourceNetwork {
	
	@JsonProperty("source-ip")
	private String srcIp;	
	
	@JsonProperty("source-netmask")
	private String srcNetmask;

	public String getSrcIp() {
		return srcIp;
	}

	public void setSrcIp(String srcIp) {
		this.srcIp = srcIp;
	}

	public String getSrcNetmask() {
		return srcNetmask;
	}

	public void setSrcNetmask(String srcNetmask) {
		this.srcNetmask = srcNetmask;
	}
	
}
