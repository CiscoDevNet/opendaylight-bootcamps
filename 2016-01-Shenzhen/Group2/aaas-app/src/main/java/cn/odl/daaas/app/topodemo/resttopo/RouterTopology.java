package cn.odl.daaas.app.topodemo.resttopo;

import java.util.ArrayList;

import org.codehaus.jackson.annotate.JsonIgnoreProperties;
import org.codehaus.jackson.annotate.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown=true)
public class RouterTopology 
{
	@JsonProperty("topology-id")
	private String topologyId;
	
	private ArrayList<Link> links;
	
	private ArrayList<Node> nodes;

	public String getTopologyId() {
		return topologyId;
	}

	public void setTopologyId(String topologyId) {
		this.topologyId = topologyId;
	}

	public ArrayList<Link> getLink() {
		return links;
	}

	public void setLink(ArrayList<Link> link) {
		this.links = link;
	}

	public ArrayList<Node> getNode() {
		return nodes;
	}

	public void setNode(ArrayList<Node> node) {
		this.nodes = node;
	}	
}
