

function open_chat_area(chat_box_id,elem){
    const chat_area = document.querySelector('.chat-area');
    close_details_area();
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

function load_conv_area(){
    console.log('START ');
    $.ajax({
        url: '/load-conv-area/',
        type: 'GET',
        data:{},
        dataType: "json",
        success: function(data) {
            console.log('code ',data.code);
            if(data.code == 201){
                $('#conversation-area').html(data.html);
            }
        }
    })
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

    $.ajax({
        url: "/add-conv/",
        type: "GET",
        data:{'chat_box_id':box_ID},
        dataType: "json",
        success: function(data){
            $('#detail-area').css('display','block');
            $('#detail-area').html(data.html);
        },
        
    });


    $('#conversation-area').html('');
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





