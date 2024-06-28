

const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");



chatSocket.onmessage = function (e) {
    console.log('good 1');
    const data = JSON.parse(e.data);
    const message = data['message'];
    const userProfilePic = data['userProfilePic'];

    console.log('good 2');
    document.querySelector("#text_input").value = "";
    var newMessage = `
        <div class="chat-msg ">
            <div class="chat-msg-profile">
                <img class="chat-msg-img" src="${userProfilePic}" alt="">
                <div class="chat-msg-date">just now</div>
            </div>
            <div class="chat-msg-content">
                <div class="chat-msg-text">${message}</div>

            </div>
        </div>
        `;
    $("#chat_main_area_id").append(newMessage);
    console.log('good3');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// Send message to server

function sendMessage(){
    var messageInput = document.querySelector("#text_input").value;
    
    console.log(messageInput);
    chatSocket.send(JSON.stringify({ 
        'message': messageInput, 
        'email' : USER_email,
        //'userProfilePic':String(userProfilePic),


    }));
    
    
};



