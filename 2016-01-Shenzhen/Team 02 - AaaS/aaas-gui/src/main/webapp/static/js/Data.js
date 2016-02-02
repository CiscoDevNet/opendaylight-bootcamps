var topologyData; 
$(function (){			    	
	$.ajax({
        url:'/daas-app/daas',
        type:'get',
        dataType:'json',	        
        data:{},
        async:false,
        success:function(data)
        {
        	if(data){
        		topologyData = data;
        	}
        }		
});
});