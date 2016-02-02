<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>topology modification</title>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/jquery-1.8.0.min.js"></script>
<script type="text/javascript">
	
	$(function() {
		$("#aDDBtn").on("click", function() {
			$.ajax({
				url : '/daas-app/daasmod/add',
				type : 'get',
				dataType : 'json',
				data : {
					"odlIpAddr" : $("#odlIpAddr").attr("value"),
					"daassrcIp" : $("#daassrcIp").attr("value"),
					"srcPort" : $("#srcPort").attr("value"),
					"srcNetmask" : $("#srcNetmask").attr("value"),
					"daasdestIp" : $("#daasdestIp").attr("value"),
					"dstPort" : $("#dstPort").attr("value"),
					"destNetmask" : $("#destNetmask").attr("value"),
					"protocol" : $("#protocol").attr("value"),
					"ruleId" : $("#ruleId").attr("value"),
					"daasaction" : $("#daasaction").attr("value")
				},
				async : true,
				success : function(data) {
					alert("Add Success!");
				}
			});
		});
	});
</script>
</head>
<body>
<p>OpenDayLight controller IP_ADDR: <input type="text" name="odlIpAddr" id="odlIpAddr" value="127.0.0.1"/></p>
<p>Daaas source Ip: <input type="text" name="daassrcIp" id="daassrcIp" value="1.1.1.1"/> &nbsp;
   Daaas source Ip port: <input type="text" name="srcPort" id="srcPort" value="8080"/>&nbsp;
   Daaas source Ip netmask: <input type="text" name="srcNetmask" id="srcNetmask" value="255.255.254.0"/>&nbsp;
</p>
<p>Daaas target Ip: <input type="text" name="daasdestIp" id="daasdestIp" value="2.3.1.1"/> &nbsp;
   Daaas target Ip port: <input type="text" name="dstPort" id="dstPort"  value="8080"/> &nbsp;
   Daaas target Ip netmask: <input type="text" name="destNetmask" id="destNetmask" value="255.255.254.0"/>
</p>
<p>Daaas   Protocol: <input type="text" name="protocol" id="protocol"  value="tcp"/></p>
<p>Daaas     Action: <input type="text" name="daasaction" id="daasaction" value="deny"/></p>
<p>Daaas     ruleId: <input type="text" name="ruleId" id="ruleId" value="deny"/></p>

<input type="button" id="aDDBtn" value="Add"/>
</body>
</html>