from django.shortcuts import render
from django.shortcuts import redirect , get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse
from django.core import serializers
from .models import USER
from .models import chats,chat_msg ,chat_file

from django.utils import timezone
from datetime import datetime
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
            return JsonResponse({'status': 'redirection',
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
    
def SignUP(request):
    return render(request,'html/signup.html')

@login_required
def LogoutU(request):
    logout(request)
    return redirect("home")
    #return render(request,'html/login.html')

@login_required
def HOME(request):
    user_L=request.user
    chat_msg_data = chat_msg.objects.all()
    chats_data = chats.objects.all()

    Chats_Data=[]
    for cd in chats_data:
        chats_users= cd.chats_users

        other_user_email=''
        if  user_L.email in chats_users.split():
            for chats__users in chats_users.split():
                if not chats__users == user_L.email:

                    other_user_email = chats__users
            


        if not cd.grp :
            try:
                other_user_data = USER.objects.get(email=other_user_email)
                img = getattr(other_user_data,'profile_pic')
                firstname = getattr(other_user_data,'firstname')
                lastname = getattr(other_user_data,'lastname')
                username = getattr(other_user_data,'username')
                title=username
            except:
                img = ''
                title =''
        else:
            img =cd.img
            title=cd.title

        
        last_msg_Data = chat_msg.objects.filter(chat_box_id=cd.chat_box_id).order_by('-chat_date')[0]
        last_msg=last_msg_Data.chat
        last_msg_time=last_msg_Data.chat_date
        
        Chats_Data+=[{
                'chat_box_id':cd.chat_box_id,
                'title':title,
                'chats_users':cd.chats_users,
                'img':img,
                'grp':cd.grp,
                'last_msg':last_msg,
                'last_msg_time':last_msg_time,
            }]
        
    #Chats_Data.sort(key=lambda x: x['last_msg_time'], reverse=True)
    Chats_Data_sorted = sorted(Chats_Data, key=lambda x: x['last_msg_time'], reverse=True)


    return render(request,'html/home.html',{'chat_msg_data':chat_msg_data,
                                            'chats_data':Chats_Data_sorted,})

@login_required
def open_conv(request):
    user_L=request.user
    if request.method == "GET":
        chat_box_id =request.GET.get('chat_box_id')

        try:
            chats_data = chats.objects.get(chat_box_id=chat_box_id)
            check_user = getattr(chats_data,'chats_users')
            if(user_L.email in check_user or user_L.email in check_user.split()):
                
                chat_msg_D = chat_msg.objects.filter(chat_box_id=chat_box_id).order_by('chat_date')
                #chat_msg_data = serializers.serialize('json', chat_msg_data)
                chat_msg_data=[]
                for cmd in   reversed(chat_msg_D) :
                    file = cmd.file.url if cmd.file else " "
                    sender_profile = USER.objects.get(email=cmd.user)
                    sender_profile_pic = getattr(sender_profile,'profile_pic')
                    print('sender_profile_pic.url',sender_profile_pic.url)
                    chat_msg_data+=[{
                        'chat_msg_id':cmd.chat_msg_id,
                        'chat_box_id':cmd.chat_box_id,
                        'user':cmd.user,
                        'chat_date':cmd.chat_date,
                        'contain_txt':cmd.contain_txt,
                        'chat':cmd.chat,
                        'contain_file':cmd.contain_file,
                        'file_type':cmd.file_type,

                        'file_url': file ,
                        'contain_files':cmd.contain_files,
                        'files_id':cmd.files_id,

                        'sender_profile_pic':(sender_profile_pic.url),
                    },]



                other_user_email=''
                for chats__users in check_user.split():
                    if not chats__users == user_L.email:
                        other_user_email = chats__users

                if not chats_data.grp :
                    try:
                        other_user_data = USER.objects.get(email=other_user_email)
                        img = getattr(other_user_data,'profile_pic')
                        firstname = getattr(other_user_data,'firstname')
                        lastname = getattr(other_user_data,'lastname')
                        username = getattr(other_user_data,'username')
                        title=username
                    except:
                        img = ''
                        title =''
                else:
                    img =chats_data.img
                    title=chats_data.title

                cd = {
                        'chat_box_id':chats_data.chat_box_id,
                        'title':title,
                        'chats_users':chats_data.chats_users,
                        'img':img.url,
                        'grp':chats_data.grp,
                        'last_msg':chats_data.last_msg,
                        'last_msg_time':chats_data.last_msg_time,
                    }

                box_ID= chats_data.chat_box_id
                return JsonResponse({'status': 'success',
                        'code':201,
                        'description':'',
                        'chat_msg_data':chat_msg_data,
                        'cd':cd,
                        'chat_box_id':chats_data.chat_box_id,
                        'box_ID':box_ID,
                    }, safe=False)
        except:
            return JsonResponse({'status': 'error',
                        'code':403,
                        'description':'Access denied! User not found'}, safe=False)


        
    return JsonResponse({'status': 'error',
                        'code':400})




def custom_timesince(value):
    if not isinstance(value, datetime):
        return value

    # Convert naive datetime to aware datetime
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    now = timezone.now()
    time_diff = now - value

    sec =time_diff.total_seconds()
    minutes = float(time_diff.total_seconds() // 60)
    hours = float(minutes // 60)
    day = float(hours // 24)
    month=float(day // 30)
    year=float(month // 12)


    # Custom formatting based on the time difference
    if year>0:
        if year == 1:
            return f"{int(year)} year ago"
        else:
            return f"{int(year)} years ago"
    elif month>0:
        if month == 1:
            return f"{int(month)} month ago"
        else:
            return f"{int(month)} months ago"
    elif day>0:
        if day ==1:
            return f"{int(day)} day ago"
        else:
            return f"{int(day)} days ago"
    elif hours > 0 and hours < 24:
        if ((minutes+15)//60 > hours):
            return f"{int(hours+1)}h ago"
        else:
            return f"{int(hours)}h ago"
    
    elif minutes < 60:
        return f"{int(minutes)}min ago"
    elif minutes < 1:
        return "just now"
    else:
        return f"{time_diff} ago"
