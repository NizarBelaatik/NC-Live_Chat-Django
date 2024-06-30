

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
    var fileInput = document.querySelector("#file_input").value;

    if(fileInput.files.length>0){
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('chat_box_id', chat_box_id);
        var tr_disabled_id = '#tr_'+cellId;
        $('.chat-area-footer').find('input, select, textarea, button').prop('disabled', true);
        $.ajax({
    
            url: '/open-conv/',
    
            type: 'POST',
    
            data:formData,
            processData: false, 
            contentType: false,
    
            success: function(data) {
                var new_chat_area="";
                if(data.code == 201){
    
                    //var chatData = JSON.parse(data.chat_msg_data);
                    renderChatMessages(data.chat_msg_data,data.cd,data.box_ID);
                }
            }
        })
    }

    chatSocket.send(JSON.stringify({ 
        'message': messageInput, 
        'email' : USER_email,
        //'userProfilePic':String(userProfilePic),


    }));
    
    
};



