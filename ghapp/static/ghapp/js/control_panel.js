
let url = "/ghapp/commands/";

let lights_state = false;
let fan_state = false;
let vent_state = false;

$(function(){
	$("#lights_button").click(function(){
		console.log("lights clicked");
	    if (!lights_state){
	    	console.log("turning lights on");
	    	$.post(url,{"command":101},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#lights_response_label").text(JSON.stringify(data));
	    		lights_state = true;
	    	});
	    }else{
	    	console.log("turning lights off");
	    	$.post(url,{"command":100},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#lights_response_label").text(JSON.stringify(data));
	    		lights_state = false;
	    	});
	    }
	});
	$("#fan_button").click(function(){
		console.log("fan clicked");
	    if (!fan_state){
	    	console.log("turning fan on");
	    	$.post(url,{"command":401},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#fan_response_label").text(JSON.stringify(data));
	    		fan_state = true;
	    	});
	    }else{
	    	console.log("turning fan off");
	    	$.post(url,{"command":400},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#fan_response_label").text(JSON.stringify(data));
	    		fan_state = false;
	    	});
	    }
	});
	$("#pump_button").click(function(){
		console.log("turning pump on");
		$("#pump_response_label").text(" ");
	    $.post(url,{"command":300},function(data, status){
			console.log(JSON.stringify(data));
			$("#pump_response_label").text(JSON.stringify(data));
		});
	});
	$("#vent_button").click(function(){
		console.log("vent clicked");
	    if (!vent_state){
	    	console.log("opening vent");
	    	$.post(url,{"command":201},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#vent_response_label").text(JSON.stringify(data));
	    		vent_state = true;
	    	});
	    }else{
	    	console.log("closing vent");
	    	$.post(url,{"command":200},function(data, status){
	    		console.log(JSON.stringify(data));
	    		$("#vent_response_label").text(JSON.stringify(data));
	    		vent_state = false;
	    	});
	    }
	});
});