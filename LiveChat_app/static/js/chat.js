

const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");



chatSocket.onmessage = function (e) {
    console.log('good 1');
    const data = JSON.parse(e.data);
    const message = data['message'];
    const userProfilePic = data['userProfilePic'];
    const email_sender = data['email'];
    document.querySelector("#text_input").value = "";
    var owner_chat ="";
    console.log('email_sender',email_sender);
    console.log('USER_email',USER_email);
    if(email_sender == USER_email){
        owner_chat="owner";
    }
    var newMessage = `
        <div class="chat-msg ${owner_chat}">
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



