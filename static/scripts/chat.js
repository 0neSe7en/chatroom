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
            $(".user").replaceWith(json_data.info.map(parse_user).join(''));
            //$("#users").html(json_data.info.map(parse_user).join(''))
        }
        console.log("Message is coming", json_data);
    };

    websocket.onerror = function(evt){
        console.log("Error...");
    };

    $('form').submit(function(){
        submit_button = $("#send-text");
        websocket.send(submit_button.val());
        this.reset();
        return false;
    })
});

function parse_message(message){
    date = new Date(message.date);
    date_code = '<span class="label round secondary">' + date.toLocaleString() + '</span>';
    user_code = '<span class="username">' + message.username + '</span>';
    message_code = '<span class="message">' + message.message + '</span>';
    return '<li>' + user_code + date_code + message_code + '</li>'
}

function parse_user(user){
    console.log(user);
    return '<li class="user"><a href="#">'+user.username+'</a></li>'
}