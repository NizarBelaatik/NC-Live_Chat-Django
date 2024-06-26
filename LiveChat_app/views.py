from django.shortcuts import render
from django.shortcuts import redirect , get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect


# Create your views here.


@csrf_protect
def LoginU(request):

    if request.method == "POST":
        usernameU =request.POST.get('username')
        passwordU =request.POST.get('password')
        user = authenticate(username=usernameU,password=passwordU)
        if user is not None:
            login(request,user)
            return redirect("/")
    return render(request,'html/login.html')

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
    return redirect("main_page")
    #return render(request,'html/login.html')

def home(request):

    return render(request,'html/login.html')

def SignUP(request):

    return render(request,'html/signup.html')
