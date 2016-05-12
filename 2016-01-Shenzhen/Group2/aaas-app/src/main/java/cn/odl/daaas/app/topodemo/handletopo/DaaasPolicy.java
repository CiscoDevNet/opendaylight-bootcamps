package cn.odl.daaas.app.topodemo.handletopo;

import java.util.ArrayList;

import org.codehaus.jackson.annotate.JsonProperty;

public class DaaasPolicy {
	
	@JsonProperty("acl-entry")
	private ArrayList<AclEntry> acls;

	public ArrayList<AclEntry> getAcls() {
		return acls;
	}

	public void setAcls(ArrayList<AclEntry> acls) {
		this.acls = acls;
	}
}
