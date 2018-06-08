
var url = "http://raspi/ghapp/commands/";

var lights_state = false;
$("#lights_button").click(function(){
	console.log("clicked");
    if (!lights_state){
    	console.log("turning lights on");
    	$.post(url,{"command":101},function(data, status){
    		//alert(data);
    		console.log(data);
    		$("#response_label").text(data);
    		lights_state = true;
    	});
    }else{
    	console.log("turning lights off");
    	$.post(url,{"command":100},function(data, status){
    		alert(data);
    		$("#response_label").text(data);
    		lights_state = false;
    	});
    }
});