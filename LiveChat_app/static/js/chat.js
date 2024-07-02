$("#text_input").submit(function(){
    $("#sendMessage").click();

});
var input = document.getElementById("text_input");
input.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
        $("#sendMessage").click();
    }
  });

function keypressInBox(){
    $("#sendMessage").click();

}


const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");



chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const html = data['html'];

    $("#chat_main_area_id").prepend(html);
    $('.chat-area-footer').find('input, select, textarea, button').prop('disabled', false);

};

chatSocket.onclose = function(e) {
};

// Send message to server

function sendMessage(chat_box_id){
    var messageInput = document.querySelector("#text_input").value;
    var fileInput = document.querySelector("#file-input").value;
    //var fileInput = document.querySelector("#file_input").value;

    if(messageInput){ //fileInput.files.length
        var formData = new FormData();
        //var csrfToken =  document.querySelector("file[name=csrfmiddlewaretoken]");
        var csrfToken = $("[name=csrfmiddlewaretoken]").val();
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('chat_box_id', chat_box_id);
        //var tr_disabled_id = '#tr_';
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
                }
            }
        })
    }



    chatSocket.send(JSON.stringify({ 
        'message': messageInput, 
        'email' : USER_email,
        'chat_box_id':chat_box_id,
        //'userProfilePic':String(userProfilePic),


    }));
    
    
};



