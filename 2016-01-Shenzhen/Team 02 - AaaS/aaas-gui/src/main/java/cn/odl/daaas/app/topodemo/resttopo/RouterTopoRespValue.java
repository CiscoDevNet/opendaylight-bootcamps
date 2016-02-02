package cn.odl.daaas.app.topodemo.resttopo;

import java.util.ArrayList;

import org.codehaus.jackson.annotate.JsonProperty;


public class RouterTopoRespValue
{
    @JsonProperty("topology")
    private ArrayList<RouterTopology> topology;

	public ArrayList<RouterTopology> getTopology() {
		return topology;
	}

	public void setTopology(ArrayList<RouterTopology> topology) {
		this.topology = topology;
	}
}
