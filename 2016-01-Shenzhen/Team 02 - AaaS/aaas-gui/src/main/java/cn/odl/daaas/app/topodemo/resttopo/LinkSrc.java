package cn.odl.daaas.app.topodemo.resttopo;

import org.codehaus.jackson.annotate.JsonProperty;

public class LinkSrc {
	
	@JsonProperty("source-node")
	private String sourceNode;
	
	@JsonProperty("source-tp")
	private String sourceTp;

	public String getSourceNode() {
		return sourceNode;
	}

	public void setSourceNode(String sourceNode) {
		this.sourceNode = sourceNode;
	}

	public String getSourceTp() {
		return sourceTp;
	}

	public void setSourceTp(String sourceTp) {
		this.sourceTp = sourceTp;
	}

}
