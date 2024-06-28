function open_conv(chat_box_id){
    const chat_area = document.querySelector('.chat-area');

    
    var formData = new FormData();
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
    var chatHeaderArea = $('#chat_header_area_id');
    const chat_area = document.querySelector('.chat-area');

    chatMainArea.empty();  // Clear existing messages
    chatHeaderArea.innerHTML= " nothing";

    data.forEach(function(item) {
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
    
    console.log('data.chats_data');
    //var chats_data = data.cd[0];
    console.log('data.chats_data',data.chats_data);
    console.log('data.chats_data[0]',data.chats_data);
    
    var header_chat_html =`
        <div class="chat-area-title">${data.title}</div>
        <div class="chat-area-group">
                  <img class="chat-area-profile" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/3364143/download+%283%29+%281%29.png" alt="" />
                  <img class="chat-area-profile" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/3364143/download+%282%29.png" alt="">
                  <img class="chat-area-profile" src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/3364143/download+%2812%29.png" alt="" />
                  <span>+4</span>
                </div>
                `

        chatHeaderArea.innerHTML =header_chat_html;
}