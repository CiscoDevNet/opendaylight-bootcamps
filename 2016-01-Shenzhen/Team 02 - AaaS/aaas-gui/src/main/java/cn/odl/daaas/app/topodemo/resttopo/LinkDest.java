package cn.odl.daaas.app.topodemo.resttopo;

import org.codehaus.jackson.annotate.JsonProperty;

public class LinkDest {
	
	@JsonProperty("dest-node")
	private String destNode;
	
	public String getDestNode() {
		return destNode;
	}

	public void setDestNode(String destNode) {
		this.destNode = destNode;
	}

	public String getDestTp() {
		return destTp;
	}

	public void setDestTp(String destTp) {
		this.destTp = destTp;
	}

	@JsonProperty("dest-tp")
	private String destTp;

}
