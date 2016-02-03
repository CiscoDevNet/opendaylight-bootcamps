

device_name_list = ["iosxrv-1", "iosxrv-2", "iosxrv-3", "iosxrv-4", "iosxrv-5", "iosxrv-6", "iosxrv-7", "iosxrv-8"];
device_source_network_data = {
	"iosxrv-1":[],
	"iosxrv-2":[],
	"iosxrv-3":[],
	"iosxrv-4":[],
	"iosxrv-5":[],
	"iosxrv-6":[],
	"iosxrv-7":[],
	"iosxrv-8":[]
}
bogon_list = ["10.0.0.0/8","172.16.0.0/12","192.168.0.0/16"]

function refresh() {
	/*
	"sourced-networks": {
		"sourced-network": [
		  {
		    "network-addr": "49.0.0.30",
		    "network-prefix": 32
		  },
		  {
		    "network-addr": "46.0.0.30",
		    "network-prefix": 32
		  },
		  {
		    "network-addr": "56.0.0.30",
		    "network-prefix": 32
		  },
		  {
		    "network-addr": "55.0.0.30",
		    "network-prefix": 32
		  }
		]
	}
	*/
	$("#TbodySourcedNetworks").empty();
	for (var i = device_name_list.length - 1; i >= 0; i--) {
		var device = device_name_list[i];
		var call_back  = function (device, data){
			var sourced_network = data["sourced-networks"]["sourced-network"];
			console.log(sourced_network);

			//Flush Local Storage.
			device_source_network_data[device]=[];
			for (var i = sourced_network.length - 1; i >= 0; i--) {
				var cidr = sourced_network[i]["network-addr"]+ "/" + sourced_network[i]["network-prefix"];
				device_source_network_data[device].push(cidr);
			};

			//Reresh Page.
			var table = $("#TableSourcedNetworks");
			innerHTML = "<tr><td>" + device + "</td>";
			for (var i = sourced_network.length - 1; i >= 0; i--) {
				innerHTML = innerHTML + "<td>" + sourced_network[i]["network-addr"]+ "/" + sourced_network[i]["network-prefix"] + "</td>";
			};
			innerHTML = innerHTML + "</tr>";
			table.append(innerHTML);
		};
		ajax_get_sourced_networks(device, call_back);
	};
	
}

function detect() {
	for (var i = bogon_list.length - 1; i >= 0; i--) {
		for (var j = device_name_list.length - 1; j >= 0; j--) {
			var source_net = device_source_network_data[device_name_list[j]];
			for (var n = source_net.length - 1; n >= 0; n--) {
				if(match_bogon(bogon_list[i], source_net[n])){
					mark_bogon(device_name_list[j],source_net[n]);
				}
			};
		};
	};
	alert("Detecting Finishing");
}

function match_bogon(bogon, net2match) {
	/*
	var reSpaceCheck = new RegExp("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\/\\d{1,2}");
    if (reSpaceCheck.test(net2match)) {
    	console.log("succ");
        //net2match.match(reSpaceCheck);
        if (RegExp.$1 == 10){
            return true;
        } else if (RegExp.$1 == 172 && RegExp.$2 >= 16 && RegExp.$2 <= 31){
			return true;
        } else if (RegExp.$1 == 192 && RegExp.$2 == 168){
			return true;		
        } else {
            return false;
    	}
    } else {
        return false;
    }
    */



    /*
 	var bogon_binary = "";
	var bogon_prefix = bogon.split("/")[1];
 	
 	var bogon_ip_digits = bogon.split("/")[0].split(".");
 	for (var i = 0; i <= bogon_ip_digits.length - 1; i++) {
 		bogon_binary += Number(bogon_ip_digits[i]).toString(2);
 	};




 	var net2match_binary = "";
	var net2match_prefix = net2match.split("/")[1];
 	
 	var net2match_ip_digits = net2match.split("/")[0].split(".");
 	for (var i = 0; i <= net2match_ip_digits.length - 1; i++) {
 		net2match_binary += Number(net2match_ip_digits[i]).toString(2);
 	};
 	*/


 	var net2match_binary = "";
 	var net2match_prefix = net2match.split("/")[1];
 	
 	var net2match_ip_digits = net2match.split("/")[0].split(".");

 	if (net2match_ip_digits[0] == 10){
 		return true;
 	} else if (net2match_ip_digits[0] == 172 && net2match_ip_digits[1] >= 16 && net2match_ip_digits[1] <= 31){
 		return true;
 	} else if (net2match_ip_digits[0] == 192 && net2match_ip_digits[1] == 168){
 		return true;
 	} else {
 		return false;
 	}
 	
 }

 function mark_bogon(device_name, source_net) {
 	var table = $("#TableSourcedNetworks");	
 	var trs = $("#TableSourcedNetworks tr");
 	for (var i = trs.length - 1; i >= 0; i--) {
 		var tds = $(trs[i]).find("td");
 		if($(tds[0]).html() == device_name){
 			for (var i = tds.length - 1; i >= 1; i--) {
 				if($(tds[i]).html() == source_net){
 					console.log(device_name, source_net);
 					$(tds[i]).append("<button type='button' class='btn btn-danger btn-xs' onclick='ajax_delete_sourced_network(\"" + device_name + "\",\"" + source_net + "\");'>del</button>")

 				}
 			}
 		}
 	};
 }

 function ajax_delete_sourced_network(device_name, delete_network) {
 	var url_to_del = "http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/"+ device_name +"/yang-ext:mount/Cisco-IOS-XR-ipv4-bgp-cfg:bgp/instance/default/instance-as/0/four-byte-as/65504/default-vrf/global/global-afs/global-af/ipv4-unicast/sourced-networks/sourced-network/" + delete_network;
 	$.ajax({ 
 		type: "DELETE",
 		dataType: "json",
 		url: url_to_del,
 		beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Basic YWRtaW46YWRtaW4=');},
 		complete: function(jqXHR){
 			console.log(jqXHR);
 			if(jqXHR["statusText"] == "OK"){
 				alert("ajax_delete_sourced_network called Succefully");
 			} else {
 				alert("error occur!");
 			}
 			refresh();	
 		}
 	});	
 }

 function ajax_get_sourced_networks(device_name, call_back){
 	var device_url = "http://localhost:8181/restconf/config/opendaylight-inventory:nodes/node/" + device_name + "/yang-ext:mount/Cisco-IOS-XR-ipv4-bgp-cfg:bgp/instance/default/instance-as/0/four-byte-as/65504/default-vrf/global/global-afs/global-af/ipv4-unicast/sourced-networks/";

 	$.ajax({ 
 		type: "GET",
 		dataType: "json",
 		url: device_url,
 		beforeSend: function(xhr){xhr.setRequestHeader('Authorization', 'Basic YWRtaW46YWRtaW4=');},
 		success: function(data){        
 			call_back(device_name, data);
 		}
 	});	
 }
