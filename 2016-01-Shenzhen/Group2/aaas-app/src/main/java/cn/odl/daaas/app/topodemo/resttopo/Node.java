package cn.odl.daaas.app.topodemo.resttopo;

import java.util.ArrayList;

import org.codehaus.jackson.annotate.JsonProperty;

public class Node 
{
	@JsonProperty("node-id")
	private String nodeId;
	
	@JsonProperty("termination-point")
	private ArrayList<NodeTermPoint> terminationPoints;
	
	@JsonProperty("l3-unicast-igp-topology:igp-node-attributes")
	private IGPNodeAttr iGPNodeAttr;

	public String getNodeId() {
		return nodeId;
	}

	public void setNodeId(String nodeId) {
		this.nodeId = nodeId;
	}

	public ArrayList<NodeTermPoint> getTerminationPoints() {
		return terminationPoints;
	}

	public void setTerminationPoints(ArrayList<NodeTermPoint> terminationPoints) {
		this.terminationPoints = terminationPoints;
	}

	public IGPNodeAttr getiGPNodeAttr() {
		return iGPNodeAttr;
	}

	public void setiGPNodeAttr(IGPNodeAttr iGPNodeAttr) {
		this.iGPNodeAttr = iGPNodeAttr;
	}
	
	
}
