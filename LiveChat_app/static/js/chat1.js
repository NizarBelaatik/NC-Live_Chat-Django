function open_conv(chat_box_id){
    const chat_area = document.querySelector('.chat-area');

    
    var formData = new FormData();
    formData.append('USER_email', USER_email);
    formData.append('chat_box_id', chat_box_id);
    
    $.ajax({

        url: '/open-conv/',

        type: 'GET',

        data:{'USER_email': USER_email,
            'chat_box_id': chat_box_id,
            },


        success: function(data) {
            var new_chat_area="";
            if(data.code == 201){

                //var chatData = JSON.parse(data.chat_msg_data);
                
                renderChatMessages(data.chat_msg_data);
            }
        }
    })
}

function renderChatMessages(data) {
    var chatMainArea = $('#chat_main_area_id');
    const chat_area = document.querySelector('.chat-area');

    chatMainArea.empty();  // Clear existing messages

    data.forEach(function(item) {
        console.log(item.file_url);
        var chat = item;
        var user = chat.user;
        var ownerClass = user == USER_email ? 'owner' : '';
        var profilePicHtml = chat.profile_pic_url ? 
                             '<img class="chat-msg-img" src="' + chat.profile_pic_url + '" alt="" />' : '';
        var fileHtml = '';

        if (chat.contain_file) {
            var fileIcon = '';
            switch(chat.file_type) {
                case 'excel':
                    fileIcon = '<i class="ri-file-excel-2-line fp_icon"></i>';
                    break;
                case 'pdf':
                    fileIcon = '<i class="bi bi-file-earmark-pdf fp_icon"></i>';
                    break;
                case 'img':
                    fileIcon = '<img src="' + chat.file_url + '" alt="Image" />';
                    break;
                case 'word':
                    fileIcon = '<i class="bi bi-file-earmark-word fp_icon"></i>';
                    break;
                default:
                    fileIcon = '<i class="ri-file-line fp_icon"></i>';
            }
            fileHtml = '<div class="chat-msg-text"><a class="nav-link nav-icon show" href="' + chat.file_url + '" download>' + fileIcon + '</a></div>';
        }

        var chatHtml = `
            <div class="chat-msg ${ownerClass}">
                <div class="chat-msg-profile">
                    ${profilePicHtml}
                    <div class="chat-msg-date">${chat.chat_date}</div>
                </div>
                <div class="chat-msg-content">
                    ${fileHtml}
                    <div class="chat-msg-text">${chat.chat} ............... ${chat.profile_pic_url}</div>
                </div>
            </div>
        `;

        chatMainArea.append(chatHtml);
    });
}