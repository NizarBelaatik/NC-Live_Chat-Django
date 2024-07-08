from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import redirect , get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse
from django.core import serializers
from .models import USER
from .models import Chats_BOX,chat_msg ,chat_file

from django.utils import timezone
from datetime import datetime

import logging
import random
import string

from collections import Counter



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

def Get_Other_User_Email(user_L,chats_users):
    other_user_email =''
    if  user_L.email in chats_users.split():
        for chats__users in chats_users.split():
            if not chats__users == user_L.email:
                other_user_email = chats__users
    return other_user_email

@login_required
def HOME(request):
    user_L=request.user
    chat_msg_data = chat_msg.objects.all()
    chats_data = Chats_BOX.objects.all()

    return render(request,'html/home.html',{'chat_msg_data':chat_msg_data,})

@login_required
def open_chat_area(request):

    user_L=request.user
    user={'email':user_L.email,
          'profile_pic':user_L.profile_pic}

    print
    if request.method == "GET":
        chat_box_id =request.GET.get('chat_box_id')
        try:
            chats_data = Chats_BOX.objects.get(chat_box_id=chat_box_id)
            check_user = getattr(chats_data,'chats_users')
            
            if(user_L.email in check_user or user_L.email in check_user.split()):
                
                chat_msg_D = chat_msg.objects.filter(chat_box_id=chat_box_id).order_by('chat_date')
                chat_msg_data=[]
                for cmd in   reversed(chat_msg_D) :
                    #files_id = cmd.contain_file if cmd.file else " "
                    files=[]
                    if cmd.contain_file :
                        file_data = chat_file.objects.filter(chat_box_id=chat_box_id, chat_file_id=cmd.files_id)
                        if len(file_data)>0:
                            file_data=file_data[0]
                            files={
                                'file_check':True,
                                'file_index':0,
                                'file':file_data.file,
                                'file_type':file_data.file_type,
                                'file_date':file_data.file_date,
                                'files_id':file_data.files_id,}
                            
                    elif cmd.contain_files :
                        
                        file_data = chat_file.objects.filter(chat_box_id=chat_box_id, chat_file_id=cmd.files_id)
                        index=0
                        for f_D  in file_data:
                            
                            files+=[{
                                'file_check':True,
                                'file_index':index,
                                'file':f_D.file,
                                'file_type':f_D.file_type,
                                'file_date':f_D.file_date,
                                'files_id':f_D.files_id,}]
                            
                            index+=1
                        
                                
                    else:
                        files=[{'file_check':False}]
                        
                    
                    
                    
                    try:
                        sender_profile = USER.objects.get(email=cmd.user)
                        sender_profile_pic = getattr(sender_profile,'profile_pic')
                    except:
                        sender_profile_pic=''
                    
                    
                    chat_msg_data+=[{
                        'chat_msg_id':cmd.chat_msg_id,
                        'chat_box_id':cmd.chat_box_id,
                        'user':cmd.user,
                        'chat_date':cmd.chat_date,
                        'contain_txt':cmd.contain_txt,
                        'chat':cmd.chat,
                        'contain_file':cmd.contain_file,

                        'contain_files':cmd.contain_files,
                        'files_id':cmd.files_id,

                        'sender_profile_pic':sender_profile_pic,
                        
                        'files':files,

                    },]

                    


                other_user_email=''
                for chats__users in check_user.split():
                    if not chats__users == user_L.email:
                        other_user_email = chats__users

                
                # get data of the conversation
                if not chats_data.grp :
                    try:
                        other_user_data = USER.objects.get(email=other_user_email)
                        img = getattr(other_user_data,'profile_pic')
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
                        'img':img,
                        'grp':chats_data.grp,
                        'last_msg':chats_data.last_msg,
                        'last_msg_time':chats_data.last_msg_time,
                    }

                
                box_ID= chats_data.chat_box_id
    
                html = render_to_string('html/chat_box/chat_area.html', {
                            'user':user,
                            'chat_msg_data':chat_msg_data,
                            'Chats_BOX':cd,
                            'box_ID':box_ID,}
                            , request=request)
                return JsonResponse({'status': 'success',
                                    'code':201,
                                    'description':'',
                                    'html':html,
                                    }, safe=False)

            
        except:
            return JsonResponse({'status': 'error',
                        'code':403,
                        'description':'Access denied! User not found'}, safe=False)


        
    return JsonResponse({'status': 'error',
                        'code':400})

    
@login_required
def load_conv_area(request):
    user_L=request.user
    if request.method == "GET": #request.is_ajax():
        #chat_box_id =request.GET.get('chat_box_id')

        chats_data = Chats_BOX.objects.all()
        Chats_Data=[]
        for cd in chats_data:
            chats_users= cd.chats_users

            other_user_email=Get_Other_User_Email(user_L,chats_users)

            if not cd.grp :
                try:
                    other_user_data = USER.objects.get(email=other_user_email)
                    img = getattr(other_user_data,'profile_pic')
                    username = getattr(other_user_data,'username')
                    title=username
                except:
                    img = ''
                    title =''
            else:
                img =cd.img
                title=cd.title

            last_msg_Data = chat_msg.objects.filter(chat_box_id=cd.chat_box_id).order_by('-chat_date')
            if len(last_msg_Data)>0:
                
                last_msg=last_msg_Data[0].chat
                last_msg_time=last_msg_Data[0].chat_date
            else:
                last_msg=''
                last_msg_time=cd.box_created_date

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


        html = render_to_string('html/chat_box/load_conv_area.html', {
                        'chats_data':Chats_Data_sorted}, 
                        request=request)
        return JsonResponse({
                    'code':201,
                    'description':'',
                    'html': html})
    
    JsonResponse({'status': 'error',
                        'code':400})


@login_required
def load_add_conv(request):
    user_L=request.user
    if request.method == "GET": #request.is_ajax():
        #chat_box_id =request.GET.get('chat_box_id')

        Chats_Data_sorted=''
        html = render_to_string('html/chat_box/load_add_conv.html', {'chats_data':Chats_Data_sorted}, 
                        request=request)
        

        return JsonResponse({
                    'code':201,
                    'description':'',
                    'html': html})
    JsonResponse({'status': 'error',
                        'code':400})
     
@login_required
def create_chat(request):
    user_L=request.user
    if request.method == "POST": #request.is_ajax():
        add_user_email =request.POST.get('email')
        chats_users=f'{user_L.email} {add_user_email}' 
        C_U_list=chats_users.split()
        get_Chats_BOX_users=Chats_BOX.objects.all()
        for u in get_Chats_BOX_users:
            cu=u.chats_users
            if Counter(cu.split()) == Counter(C_U_list):
                c_b_id=u.chat_box_id
                return JsonResponse({'status': 'error',
                        'code':201,
                        'description':'Conversation already existed',
                        'chat_box_id':c_b_id}, safe=False)


        chat_box_id=check_id_in_model(Chats_BOX,'chat_box_id')
        
        Chats_BOX.objects.create(
            chat_box_id=chat_box_id,
            chats_users=chats_users,
            grp=False,
        )
        chat_msg.objects.create(
            chat_msg_id='f{chat_box_id}_msg_01',
            chat_box_id=chat_box_id,
            user='system_01',
            contain_txt=True,
            chat='first msg',

            contain_file=False,
            contain_files=False,
        )
        return JsonResponse({
                    'code':201,
                    'description':'',
                    'chat_box_id': chat_box_id})
    JsonResponse({'status': 'error',
                        'code':400})
    
    
@login_required
def load_details_area(request):
    user_L=request.user
    if request.method == "GET": #request.is_ajax():
        chat_box_id =request.GET.get('chat_box_id')
        chats_data = Chats_BOX.objects.get(chat_box_id=chat_box_id)
        check_user = getattr(chats_data,'chats_users')
        if(user_L.email in check_user or user_L.email in check_user.split()):
            
            if not chats_data.grp :
                try:
                    other_user_email=Get_Other_User_Email(user_L,check_user)
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


            shared_image_1=chat_file.objects.filter(chat_box_id=chat_box_id).order_by('file_date')
            shared_image_2=chat_file.objects.filter(chat_box_id=chat_box_id).order_by('file_date')
            shared_image = shared_image_1
            html = render_to_string('html/chat_box/details_area.html', {
                        'chats_users':chats_data.chats_users,
                        'img':img,
                        'title':title,
                        'shared_image':shared_image,}
                        , request=request)
        try:

            
            
                
                
                return JsonResponse({
                        'code':201,
                        'description':'',
                        'html': html})
        except:
            return JsonResponse({'status': 'error',
                        'code':403,
                        'description':'Access denied! User not found'}, safe=False)
        
    return JsonResponse({'status': 'error',
                        'code':400})

@login_required
def upload_files_from_chat(request):
    user_L=request.user
    print('here111111')
    if request.method == "POST": #request.is_ajax():
        chat_box_id =request.POST.get('chat_box_id')
        #fileInput =request.FILES['fileInput']
        fileInput =request.FILES.getlist('fileInput')
        contain_txt =request.GET.get('contain_txt')

        chat_file_id = check_id_in_model(chat_file,'chat_file_id')
        files_len=0
        for file in fileInput:
            print('\nformat_file',file)
            format_file=file.name.split(".")[1]
            if format_file in ['jpg','png','jpeg','heic']:
                file_type="img"
            elif format_file in ['doc','docx']:
                file_type="word"
            elif format_file in ['xls','xlsm']:
                file_type="excel" 
            elif format_file in ['pdf']:
                file_type="pdf" 
            elif format_file in ['gif']:
                file_type="gif" 
            else:
                file_type=format_file

            files_id = check_id_in_model(chat_file,'files_id')
            chat_file.objects.create(
                chat_box_id=chat_box_id,
                chat_file_id=chat_file_id,
                files_id=files_id,
                file=file,
                file_type=file_type,
                user=user_L.email
                ) 
            files_len+=1
            
        chat_data={'chat_files_id':chat_file_id,
                   'files_len':files_len}
        print('here22222')
        return JsonResponse({
                        'code':201,
                        'description':'' ,
                        'chat_data':chat_data})
    return JsonResponse({
                        'code':400,
                        'description':'' })







def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # You can customize this for your needs
    random_string = ''.join(random.choice(characters) for _ in range(length))
    random_string=random_string.replace("%20","")
    random_string=random_string.replace(" ","")
    return random_string

def check_id_in_model(Object,column,id=generate_random_string(10)):
    col_contains = f'{column}__contains'
    
    while True:
        obj=Object.objects.filter( **{col_contains:id} )
        if  len(obj)==0 :
            return id
        id = generate_random_string(10)




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
