const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function upvote(message_id) {
    socket.send(JSON.stringify({'messageType': 'upvoteMessage', 'message_id': message_id}));
}

function addUpvote(message) {
    // console.log("adding upvote")
    let upvote = document.getElementById(message['id'].toString() + "_upvote");
    upvote.innerHTML = "Upvote [" + message['upvoteCount'] + "]";
}

socket.onmessage = function (ws_message) {
    const message = JSON.parse(ws_message.data);
    const messageType = message.messageType
    // console.log(message)
    switch (messageType) {
        case 'upvoteMessage':
            addUpvote(message);
            break
        default:
            console.log("received an invalid WS messageType");
    }
}
