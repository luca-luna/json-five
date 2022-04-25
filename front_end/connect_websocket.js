const socket = new WebSocket('ws://' + window.location.host + '/websocket');

function upvote(message_id) {
    socket.send(JSON.stringify({'messageType': 'upvoteMessage', 'message_id': message_id}));
}
