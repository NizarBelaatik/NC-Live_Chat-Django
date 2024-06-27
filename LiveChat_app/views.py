from django.shortcuts import render
from django.shortcuts import redirect , get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse

from .models import chat_msg ,chat_file
# Create your views here.

def Login(request):
    return render(request,'html/login.html')

@csrf_protect
def LoginU(request):


    if request.method == "POST":
        emailU =request.POST.get('email')
        passwordU =request.POST.get('password')
        user = authenticate(username=emailU,password=passwordU)
        if user is not None:
            login(request,user)
            return JsonResponse({'status': 'successfull',
                                 'code':300,
                                 'redirect':'/home/'})
        
    return JsonResponse({'status': 'error',
                        'code':400})

@csrf_protect
def SignupU(request):
    
    pl=False
    pm=False
    pc=False
    pn=False
    per=False
    if request.method == 'POST':
        username =request.POST.get('username')
        emailU =request.POST.get('email')
        pw1 =request.POST.get('password1')
        pw2 =request.POST.get('password2')
        
        per = True
        
        if str(pw1) == str(pw2):
            pm=True
            for i in str(pw1):
                # if string has letter
                if i in "abcdefghijklmnopqrstuvwxyz" or i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    pc = True
                # if string has number
                if i in "0123456789":
                    pn = True

        if len(str(pw1)) >= 8 :
            pl=True
            
        if pl and pm and pc and pn :
            data = User.objects.create_user(username=username, email=emailU , password=pw1)
            data.save()
            return render(request, 'html/home.html')

    return render(request, 'html/signup.html',{"per":per,"pl":pl,"pm":pm,"pc":pc,"pn":pn})
    
    
@login_required
def LogoutU(request):
    logout(request)
    return redirect("home")
    #return render(request,'html/login.html')

@login_required
def HOME(request):
    chat_msg_data = chat_msg.objects.all()
    #chat_msg_data+=[{'chat_msg_data':chat_msg_data,}]
    return render(request,'html/home.html',{'chat_msg_data':chat_msg_data})

def SignUP(request):

    return render(request,'html/signup.html')
