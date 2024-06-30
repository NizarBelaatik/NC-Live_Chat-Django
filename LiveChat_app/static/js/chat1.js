function open_conv(chat_box_id,elem){
    const chat_area = document.querySelector('.chat-area');
    
    var chatMainArea = $('#chat_main_area_id');
    var chatHeaderArea = $('#chat_header_area_id');

    chatMainArea.empty();  // Clear existing messages
    chatHeaderArea.empty();

    var all_elem_with_active=document.querySelectorAll('.msg');
    all_elem_with_active.forEach(function(aewa){
        if(aewa.classList.contains('active')){
            aewa.classList.remove("active");
        }
    })


    elem.classList.add("active");
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
            console.log('code',data.code);
            if(data.code == 201){
                $('#chat-area').html(data.html);
                
                //var chatData = JSON.parse(data.chat_msg_data);
                //renderChatMessages(data.chat_msg_data,data.cd,data.box_ID);
            }
        }
    })
}

function renderChatMessages(data,cd,box_ID) {
    var chatMainArea = $('#chat_main_area_id');
    var chatHeaderArea = $('#chat_header_area_id');
    const chat_area = document.querySelector('.chat-area');

    //var box_ID='';
    chatMainArea.empty();  // Clear existing messages
    chatHeaderArea.empty();

    var chatHtml='';
    data.forEach(function(item) {

        var chat = item;
        var user = chat.user;
        var ownerClass = user == USER_email ? 'owner' : '';
        var profilePicHtml = chat.sender_profile_pic ? 
                             '<img class="chat-msg-img" src="' + chat.sender_profile_pic + '" alt="" />' : '';
        
        var chat_msg_profile = '';

        if(user != USER_email){
            chat_msg_profile = `<div class="chat-msg-profile">
                    ${profilePicHtml}
                    <div class="chat-msg-date">${chat.chat_date}</div>
                </div>`;
        }
        
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

         chatHtml += `
            <div class="chat-msg ${ownerClass}" >
                ${chat_msg_profile}

                <div class="chat-msg-content">
                    ${fileHtml}
                    <div class="chat-msg-text">${chat.chat}</div>
                </div>
            </div>
        `;
    });


    var a = `
        
        <div class="chat-area" id="chat-area-${box_ID}">
            <div class="chat-area-header" id="chat_header_area_id">
                <img class="msg-profile" src="${cd.img}" alt="" />
                <div class="chat-area-title">${cd.title}</div>
                <div class="chat-area-group">
                    <a class="cursor_pointer" onclick="open_details_area('${box_ID}')"><i class="bx bx-cog bx-md"></i></a>
                </div>
            </div>
            <div class="chat-area-main" id="chat_main_area_id" style="overflow-y: auto;display: flex;flex-direction: column;overflow-y: auto; height:100%!important; width: 100%!important; flex-direction: column-reverse;">
                ${chatHtml}
            </div>


            <div class="chat-area-footer">
              
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-image">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <circle cx="8.5" cy="8.5" r="1.5" />
                  <path d="M21 15l-5-5L5 21" /></svg>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus-circle">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 8v8M8 12h8" /></svg>

                  
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-paperclip">
                  <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48" /></svg>
                
                <label for="file-input">
                  <a class="a_btn"><i class="fa fa-paperclip" ></i></a>
                </label>
                <input type="file" multiple  id="file-input" style="display: none;"></input>
              
                <a class="a_btn"><i class="bx bxs-face bx-sm "></i></a>
                <input type="text" id="text_input"  placeholder="Type something here..." />

                <a class="a_btn" onclick="sendMessage()"><i class="bx bx-send bx-sm btn"></i></a>

                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="feather feather-thumbs-up">
                  <path d="M14 9V5a3 3 0 00-3-3l-4 9v11h11.28a2 2 0 002-1.7l1.38-9a2 2 0 00-2-2.3zM7 22H4a2 2 0 01-2-2v-7a2 2 0 012-2h3" /></svg>
              
              
            </div>
        </div>`;
    var chat_area_id = document.querySelector('#chat-area');
    //chat_area_id.innerHTML=a;
    chatMainArea.scrollTop = chatMainArea.scrollHeight;
    

    const chatContent = document.getElementById('chat_main_area_id');
    chatContent.scrollTop = chatContent.scrollHeight;
    
        
}


function open_details_area(box_ID){
    $.ajax({
        url: "/load-details-area/",
        type: "GET",
        data:{'chat_box_id':box_ID},
        dataType: "json",
        success: function(data){
            $('#detail-area').css('display','block');
            $('#detail-area').html(data.html);
            
        },
        error: function(data){// (xhr, status, error){
            console.error("Error: " + data.code+ " | " + data.description);
        }
    });
}
function close_details_area(){
    $('#detail-area').html('');
    $('#detail-area').css('display','none');
}
function add_conv(){
    
}


document.addEventListener('DOMContentLoaded', function () {

    const popupOverlay = document.getElementById('popupOverlay');

    const popup = document.getElementById('popup');

    const closePopup = document.getElementById('closePopup');

    const emailInput = document.getElementById('emailInput');

    // Function to open the popup

    function openPopup() {

        popupOverlay.style.display = 'block';

    }

    // Function to close the popup

    function closePopupFunc() {

        popupOverlay.style.display = 'none';

    }

    // Function to submit the signup form

    function submitForm() {

        const email = emailInput.value;

        // Add your form submission logic here

        console.log(`Email submitted: ${email}`);

        closePopupFunc(); // Close the popup after form submission

    }

    // Event listeners

    // Trigger the popup to open (you can call this function on a button click or any other event)

    openPopup();

    // Close the popup when the close button is clicked

    closePopup.addEventListener('click', closePopupFunc);

    // Close the popup when clicking outside the popup content

    popupOverlay.addEventListener('click', function (event) {

        if (event.target === popupOverlay) {

            closePopupFunc();

        }

    });

    // You can customize and expand these functions based on your specific requirements.

});