package cn.odl.daaas.app.topodemo.resttopo;

import org.codehaus.jackson.annotate.JsonProperty;

public class Link 
{
	@JsonProperty("link-id")
	private String linkId;
	
	private LinkSrc source;
	
	private LinkDest destination;

	

	@JsonProperty("l3-unicast-igp-topology:igp-link-attributes")
	private IGPTopologyAttr iGPTopologyAttr;

	public String getLinkId() {
		return linkId;
	}

	public void setLinkId(String linkId) {
		this.linkId = linkId;
	}

	

	public void setiGPTopologyAttr(IGPTopologyAttr iGPTopologyAttr) {
		this.iGPTopologyAttr = iGPTopologyAttr;
	}
	
	public LinkSrc getSource() {
		return source;
	}

	public void setSource(LinkSrc source) {
		this.source = source;
	}

	public LinkDest getDestination() {
		return destination;
	}

	public void setDestination(LinkDest destination) {
		this.destination = destination;
	}

	public IGPTopologyAttr getiGPTopologyAttr() {
		return iGPTopologyAttr;
	}

	@Override
    public String toString()
    {
        String res = "linkId = "  + getLinkId() + " "
               + "source = " + getSource() + " "
               + "destination = "+ getDestination()+ " "               
               + "iGPTopologyAttr = "  + getiGPTopologyAttr();
        return res;
    }

}
