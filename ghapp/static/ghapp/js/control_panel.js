
var url = "http://raspi/ghapp/commands/"
$("#lights_button").click(function(){
    $.post(url,
    {
        command: 100
    }
});