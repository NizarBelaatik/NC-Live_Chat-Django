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
    console.log('html   ',html);
    $("#chat_main_area_id").prepend(html);
    $('.chat-area-footer').find('input, select, textarea, button').prop('disabled', false);
    document.querySelector("#text_input").value='';
};

chatSocket.onclose = function(e) {
};

// Send message to server

function sendMessage(chat_box_id){
    var messageInput = document.querySelector("#text_input").value;
    var fileInput = document.querySelector("#file-input");

    

    //var fileInput = document.querySelector("#file_input").value;
    var contain_txt='False';
    if(messageInput && messageInput !== "" && messageInput != ""){
        contain_txt="True";
    }
    var chat_files_id = "";
    var files_len = 0 ;
    if(fileInput.files.length>0){ //fileInput.files.length
        var formData = new FormData();
        //var csrfToken =  document.querySelector("file[name=csrfmiddlewaretoken]");
        var csrfToken = $("[name=csrfmiddlewaretoken]").val();
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('chat_box_id', chat_box_id);
        //formData.append('fileInput', fileInput);
        for (var i = 0; i < fileInput.files.length; i++) {
            formData.append('fileInput', fileInput.files[i]);
        }

        formData.append('contain_txt', contain_txt);

        $('.chat-area-footer').find('input, select, textarea, button').prop('disabled', true);
        $.ajax({
    
            url: '/upload-files-from-chat/',
    
            type: 'POST',
    
            data:formData,
            processData: false, 
            contentType: false,
    
            success: function(data) {
                console.log(data.code);
                if(data.code == 201){
                    console.log()
                    chat_files_id = data.chat_data.chat_files_id;
                    files_len = data.chat_data.files_len;
                    console.log(chat_files_id)
                    console.log(files_len)
                    //var chatData = JSON.parse(data.chat_msg_data);

                    console.log('chat_files_id is ',chat_files_id);
                    chatSocket.send(JSON.stringify({ 
                        'message': messageInput, 
                        'email' : USER_email,
                        'chat_box_id':chat_box_id,
                        'files_len':files_len,
                        'chat_files_id':chat_files_id,
                        //'userProfilePic':String(userProfilePic),

                    }));
                }
            }
        })
    }
    else{
        console.log('chat_files_id is is is is ',chat_files_id);
        chatSocket.send(JSON.stringify({ 
            'message': messageInput, 
            'email' : USER_email,
            'chat_box_id':chat_box_id,
            'files_len':0,
            'chat_files_id':'',
            //'userProfilePic':String(userProfilePic),
    
        }));
    }

    
    
    
};



// Preview Files 'input file select'





