<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Router information</title>
<script type="text/javascript" src="${pageContext.request.contextPath}/static/jquery-1.8.0.min.js"></script>
<script type="text/javascript">
	var routeinfo;
	$(function() {
		$("#routerBtn").on("click", function() {
			$.ajax({
				url : '/daas-app/daasqry',
				type : 'get',
				dataType : 'json',
				data : {
					"odlIpAddr" : $("#odlIpAddr").attr("value"),
					"routername" : $("#routername").attr("value")
					},
				async : false,
				success : function(data) {	
					routeinfo = JSON.stringify(data); 
					$("#rtinfo").html(routeinfo); 										
				},
				error: function(data){
					routeinfo = JSON.stringify(data); 
					$("#rtinfo").html(routeinfo); 
				}
			});
		});
	});
</script>
</head>
<body>
<p>OpenDayLight controller IP_ADDR: <input type="text" name="odlIpAddr" id="odlIpAddr"  value="127.0.0.1"/></p>
<p>Router Name: <input type="text" name="routername" id="routername"  value="sfc"/></p>

<input type="button" id="routerBtn" value="Query"/>

<label for="rtinfo" id="rtinfo"><br></label>

</body>
</html>