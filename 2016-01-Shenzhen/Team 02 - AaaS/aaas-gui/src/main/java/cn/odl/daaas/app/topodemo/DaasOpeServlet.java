package cn.odl.daaas.app.topodemo;

import java.io.IOException;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.codehaus.jackson.map.ObjectMapper;

import cn.odl.daaas.app.topodemo.handletopo.AclEntry;
import cn.odl.daaas.app.topodemo.handletopo.DaaasPolicy;
import cn.odl.daaas.app.topodemo.handletopo.DestNetwork;
import cn.odl.daaas.app.topodemo.handletopo.SourceNetwork;

public class DaasOpeServlet  extends HttpServlet{
	
	private static final long serialVersionUID = 1228448973827657725L;
	
	private static String host = "198.18.1.80";
	private static final int port = 8181;
	private static final String username = "admin";
	private static final String password = "admin";
		
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
	{ 		
		host = req.getParameter("odlIpAddr");
        String daassrcIp = req.getParameter("daassrcIp");        
        String daasdestIp = req.getParameter("daasdestIp");
        String daasaction = req.getParameter("daasaction");
        String srcPort = req.getParameter("srcPort");
        String dstPort = req.getParameter("dstPort");
        String protocol = req.getParameter("protocol");
        String srcNetmask = req.getParameter("srcNetmask");
        String destNetmask = req.getParameter("destNetmask");
        String ruleId = req.getParameter("ruleId");
        
				
		DaaasPolicy daaasPolicy = new DaaasPolicy();
		ArrayList<AclEntry> acls = new ArrayList<AclEntry>();
		AclEntry acl = new AclEntry();
		SourceNetwork sourceNetwork = new SourceNetwork();
		DestNetwork destNetwork = new DestNetwork();
		sourceNetwork.setSrcIp(daassrcIp);
		sourceNetwork.setSrcNetmask(srcNetmask);
		destNetwork.setDestIp(daasdestIp);
		destNetwork.setDestNetmask(destNetmask);
		acl.setAction(daasaction);
		acl.setDstNetwork(destNetwork);
		acl.setSrcNetwork(sourceNetwork);
		acl.setSrcPort(srcPort);
		acl.setDstPort(dstPort);
		acl.setProtocol(protocol);
		acl.setUuid(ruleId);
		acls.add(acl);
		daaasPolicy.setAcls(acls);
		
		RestReqTempateParam reqTemplateParam = new RestReqTempateParam();
		reqTemplateParam.setOdlHost(host);
		reqTemplateParam.setOdlPort(port);
		reqTemplateParam.setPassword(password);
		StringBuffer reqUrl = new StringBuffer("http://");
		reqUrl.append(host).append(":8181/restconf/config/aaas:acl-entries");
		reqTemplateParam.setRestReqUrl(reqUrl.toString());
		reqTemplateParam.setUsername(username);
		
		ObjectMapper mapper = new ObjectMapper();
		String entity = mapper.writeValueAsString(daaasPolicy);		
		reqTemplateParam.setEntity(entity);
		RestReqTemplate.doPost(reqTemplateParam);       
	}
	
	@Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
    {
		
    }

    @Override
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
    {
        ;
    }
    
    @Override
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException
    {
        ;
    }

}
