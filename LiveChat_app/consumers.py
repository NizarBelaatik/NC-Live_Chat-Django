import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User
from .models import USER
from .models import  Chats_BOX,chat_msg,chat_file

from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

import logging
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # You can customize this for your needs
    random_string = ''.join(random.choice(characters) for _ in range(length))
    random_string=random_string.replace("%20","")
    random_string=random_string.replace(" ","")
    return random_string

@database_sync_to_async
def get_user_object(email):
    return USER.objects.get(email=email)

@database_sync_to_async
def get_msg_object(Object,chat_msg_id,chat_box_id):
    return Object.objects.get(chat_msg_id=chat_msg_id,chat_box_id=chat_box_id)


@database_sync_to_async
def create_new_message(chat_msg_id, chat_box_id, user,contain_txt, chat, contain_file,contain_files , files_id):
    return chat_msg.objects.create(
        chat_msg_id=chat_msg_id,
        chat_box_id=chat_box_id,
        user=user,
        contain_txt=contain_txt,
        chat=chat,

        contain_file=contain_file,
        contain_files=contain_files,
        files_id=files_id,
    )

@database_sync_to_async
def check_id_in_model(Object,column,id=generate_random_string(10)):
    col_contains = f'{column}__contains'
    
    while True:
        obj=Object.objects.filter( **{col_contains:id} )
        if  len(obj)==0 :
            print('\n\n\n True','\n\n\n')
            return id
        id = generate_random_string(10)

class ChatConsumer(AsyncWebsocketConsumer):#AsyncWebsocketConsumer  WebsocketConsumer
    async def connect(self):
        self.roomGroupName = "chat_rooms"
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName , 
            self.channel_name #self.channel_name channel_layer
        )
    async  def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        email = text_data_json['email']

        obj_user = await get_user_object(email)
        user_profile_pic = getattr(obj_user, "profile_pic")

        chat_msg_id = await check_id_in_model(chat_msg,'chat_msg_id')
        chat_box_id = text_data_json["chat_box_id"]

        contain_txt = False
        if message:
            contain_txt = True
            
        contain_file = False
        contain_files = False

        files_id=''
        if contain_file or contain_files:
            files_id = await check_id_in_model(chat_msg,'files_id')

        await create_new_message(chat_msg_id, chat_box_id, email,contain_txt, message, contain_file,contain_files , files_id)

        #msg_data= await get_msg_object(chat_msg,chat_msg_id,chat_box_id)

        
        await self.channel_layer.group_send(
                self.roomGroupName,{
                    "type" : "sendMessage" ,
                    "email":email,
                    "userProfilePic":user_profile_pic,
                    "message":message ,
                    'chat_box_id':chat_box_id,
                    'chat_msg_id':chat_msg_id,
                    
                })
        


    async def sendMessage(self , event) : 
        user_ = self.scope.get('user')
        email = event["email"]
        #userProfilePic = event["userProfilePic"]
        message = event["message"]
        chat_box_id = event["chat_box_id"]
        chat_msg_id = event["chat_msg_id"]
       

        obj_user = await get_user_object(email)
        user_profile_pic = getattr(obj_user, "profile_pic")

        if message:
            await self.send(text_data = json.dumps({
                                                    "email":email,
                                                    "userProfilePic":user_profile_pic.url,
                                                    "message":message,
                                                    "chat_box_id":chat_box_id}))

