/**
 * Created by 0neSe7en on 2015/4/7.
 */
$(document).ready(function() {
    var wshost = 'ws://localhost:8000';
    var websocket = new WebSocket(wshost+window.location.pathname+'/update');

    websocket.onopen = function(evt){
        console.log("Connect...");
        //websocket.send("ccc");
    };

    websocket.onmessage = function(evt){
        var json_data = JSON.parse(evt.data);
        if (json_data.type=='message'){
            $("#messages").append(json_data.info.map(parse_message))
        }
        else if (json_data.type=='user_status'){
            $("#users").html(json_data.info.map(parse_user).join(''))
        }
        console.log("Message is coming", json_data);
    };

    websocket.onerror = function(evt){
        console.log("Error...");
    };

    $('form').submit(function(){
        submit_button = $(this).find('input.message');
        websocket.send(submit_button.val());
        this.reset();
        return false;
    })
});

function parse_message(message){
    return "<li><h4>" + message.username + "</h4><small>" + message.date + "</small><p>" + message.message + "</p></li>"
}

function parse_user(user){
    console.log(user);
    return "<li>"+user.username+"</li>"
}