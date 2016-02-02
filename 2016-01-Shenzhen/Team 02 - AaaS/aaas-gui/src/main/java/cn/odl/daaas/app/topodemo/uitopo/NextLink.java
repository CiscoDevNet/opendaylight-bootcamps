package cn.odl.daaas.app.topodemo.uitopo;

public class NextLink {
	
	private String source;
	private String target;
	public String getSource() {
		return source;
	}
	public void setSource(String source) {
		this.source = source;
	}
	public String getTarget() {
		return target;
	}
	public void setTarget(String target) {
		this.target = target;
	}
	
	@Override
    public String toString()
    {
        String res = "source = "  + getSource() + " "                           
               + "target = "  + getTarget() + "\n";
        return res;
    }
}
