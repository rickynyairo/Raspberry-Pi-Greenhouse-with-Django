
var url = "/ghapp/commands/";

var lights_state = false;

$(document).ready(function(){
	$("#lights_button").click(function(){
		console.log("clicked");
	    if (!lights_state){
	    	console.log("turning lights on");
	    	$.post(url,{"command":101},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#response_label").text(JSON.stringify(data));
	    		lights_state = true;
	    	});
	    }else{
	    	console.log("turning lights off");
	    	$.post(url,{"command":100},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#response_label").text(JSON.stringify(data));
	    		lights_state = false;
	    	});
	    }
	});
	}
);