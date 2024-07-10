
$("#text_input").submit(function(){
    

});

$("#text_input").addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
        
    }
  });



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

    if(elem){
        elem.classList.add("active");
    }

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
                $('#chat-area').html(data.html);
                
                //var chatData = JSON.parse(data.chat_msg_data);
                //renderChatMessages(data.chat_msg_data,data.cd,data.box_ID);
            }
        }
    })
}

function load_conv_area(){
    $.ajax({
        url: '/load-conv-area/',
        type: 'GET',
        data:{},
        dataType: "json",
        success: function(data) {
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

function load_add_conv(){
    id="conv-area-search-output"
    $.ajax({
        url: "/add-conv/",
        type: "GET",
        data:{'chat_box_id':'box_ID'},
        dataType: "json",
        success: function(data){
            $('#conversation-area').html(data.html);
        },
        
    });
}



function onchange_input_CAS(){
    var search_key_word=$('#input-conv-area-search').val();
    $.ajax({
        url: "/load-Profile-search/",
        type: "GET",
        data:{'search_key_word':search_key_word},
        dataType: "json",
        success: function(data){
            $('#load_Profile_search').html(data.html);
        },
        
    });
}


function create_chat(email){
    var formData = new FormData();
    var csrfToken = $("[name=csrfmiddlewaretoken]").val();
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('email', email);
    $.ajax({
        url: "/create-chat/",
        type: "POST",
        data:formData,
        processData: false, 
        contentType: false,
        success: function(data){
            open_chat_area(data.chat_box_id)
        },
        
    });
}







  