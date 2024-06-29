

const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");



chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const message = data['message'];
    const userProfilePic = data['userProfilePic'];
    const email_sender = data['email'];
    document.querySelector("#text_input").value = "";
    var owner_chat ="";
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
};

chatSocket.onclose = function(e) {
};

// Send message to server

function sendMessage(){
    var messageInput = document.querySelector("#text_input").value;
    
    chatSocket.send(JSON.stringify({ 
        'message': messageInput, 
        'email' : USER_email,
        //'userProfilePic':String(userProfilePic),


    }));
    
    
};



