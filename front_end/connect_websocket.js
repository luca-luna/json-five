const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function upvote(message_id) {
    socket.send(JSON.stringify({'messageType': 'upvoteMessage', 'message_id': message_id}));
}

//perhaps first step to setting up websocket DMs... but where is this set up
function directMessage() {
    socket.send(JSON.stringify({'messageType': 'directMessage', 'reciever': username}));
}

function showPrompt(){
    prompt("YO!")
}

function addUpvote(message) {
    // console.log("adding upvote")
    let upvote = document.getElementById(message['id'].toString() + "_upvote");
    upvote.innerHTML = "Upvote [" + message['upvoteCount'] + "]";
}

function broadcastDirectMessage(message){
    console.log("broadcasting direct message")
    alert("You've received a DM!");
}

socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType
    // console.log(message)
    switch (messageType) {
        case 'upvoteMessage':
            addUpvote(message);
            break
        case 'directMessage':
            //need to tell it what to do when it gets a direct message
            broadcastDirectMessage(message)
            break
        default:
            console.log("received an invalid WS messageType");
    }
}
