const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function upvote(message_id) {
    socket.send(JSON.stringify({'messageType': 'upvoteMessage', 'message_id': message_id}));
}

//perhaps first step to setting up websocket DMs... but where is this set up
function directMessage(message, username_online) {
    socket.send(JSON.stringify({'messageType': 'directMessage', 'message': message, 'recipient': username_online}))
    console.log(username_online)
}

function showPrompt(username_online){
    let capturedDirectMessage = prompt("Enter your Direct Message")
    directMessage(capturedDirectMessage, username_online)
    console.log(username_online)
}

function addUpvote(message) {
    // console.log("adding upvote")
    let upvote = document.getElementById(message['id'].toString() + "_upvote");
    upvote.innerHTML = "Upvote [" + message['upvoteCount'] + "]";
}

function broadcastDirectMessage(message){
    alert(message);
}

socket.onmessage = function (ws_message) {
    console.log("TEST")
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType
    // console.log(message)
    switch (messageType) {
        case 'upvoteMessage':
            addUpvote(message);
            break
        case 'directMessage':
            //console.log("Check me")
            //need to tell it what to do when it gets a direct message
            alertText = message.message + "\n" + "Sent by: " + message.sender
            broadcastDirectMessage(alertText)
            document.getElementById(message.sender + "_message").innerHTML = "Reply";
            document.getElementById(message.sender + "_message").style.backgroundColor = "salmon";
            document.getElementById(message.sender + "_message").style.color = "white";
            document.getElementById(message.sender + "_message").style.cssText = "animation-duration: .75s; animation-name: recent;"
            document.getElementById(message.sender + "_message").style.backgroundColor = "salmon";
            document.getElementById(message.sender + "_message").style.color = "white";
            break
        default:
            console.log("received an invalid WS messageType");
    }
}
