package cn.odl.daaas.app.topodemo.uitopo;

public class NextNode {
	private String id;
	private Integer x;
	private Integer y;
	private String name;
	
	public Integer getX() {
		return x;
	}
	public void setX(Integer x) {
		this.x = x;
	}
	public Integer getY() {
		return y;
	}
	public void setY(Integer y) {
		this.y = y;
	}
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	
	@Override
    public String toString()
    {
        String res = "id = "  + getId() + " "
               + "x = " + getX() + " "
               + "y = "+ getY()+ " "               
               + "name = "  + getName()  + "\n";
        return res;
    }
}
