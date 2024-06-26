const forms = document.querySelector(".forms"),
pwShowHide = document.querySelectorAll(".eye-icon"),
links = document.querySelectorAll(".link");
pwShowHide.forEach(eyeIcon => {
    eyeIcon.addEventListener("click", () => {

        let pwFields = eyeIcon.parentElement.querySelectorAll(".password");
        
        pwFields.forEach(password => {
            if(password.type === "password"){
                password.type = "text";
                eyeIcon.classList.replace("bx-hide", "bx-show");
                return;
            }
            password.type = "password";
            eyeIcon.classList.replace("bx-show", "bx-hide");
        })
        
    })
})    


const login_btn=document.querySelector("button[name='login']");
login_btn.addEventListener("click", ()=>{
//$("#loginForm").submit(function(){
    console.log('submited');
    var csrfToken =$("[name=csrfmiddlewaretoken]").val();
    var email = $("[name=email]").val();
    var password = $("[name=password]").val();

    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('email', email);
    formData.append('password', password);
    $.ajax({

        url: '/LoginU/',

        type: 'POST',

        data:formData,

        processData: false,

        contentType: false,

        success: function(data) {
            console.log('code',data.code);
            if(data.code == 300){
                console.log('redirect',data.redirect);
                window.location.href=data.redirect;
            }
        }
    })
})