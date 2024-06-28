import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User
from .models import USER
from .models import  chats,chat_msg,chat_file

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
def create_new_message(chat_msg_id, chat_box_id, user,contain_txt, chat, contain_file, file_type, file,contain_files , files_id):
    return chat_msg.objects.create(
        chat_msg_id=chat_msg_id,
        chat_box_id=chat_box_id,
        user=user,
        contain_txt=contain_txt,
        chat=chat,

        contain_file=contain_file,
        file_type=file_type,
        file=file,

        contain_files=contain_files,
        files_id=files_id,
    )



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
        print('email',email)
        await self.channel_layer.group_send(
                self.roomGroupName,{
                    "type" : "sendMessage" ,
                    "email":text_data_json['email'],
                    "userProfilePic":user_profile_pic,
                    "message":message 
                })

    async def sendMessage(self , event) : 
        user_ = self.scope.get('user')
        email = event["email"]
        #userProfilePic = event["userProfilePic"]
        message = event["message"]

       

        obj_user = await get_user_object(email)
        user_profile_pic = getattr(obj_user, "profile_pic")
        if message:
            await self.send(text_data = json.dumps({
                                                    "email":email,
                                                    "userProfilePic":user_profile_pic.url,
                                                    "message":message }))



class ChatConsumer_2(AsyncWebsocketConsumer):
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
    async def receive(self, text_data):
        user_ = self.scope.get('user')

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        email = text_data_json["email"]
        username = text_data_json["username"]
        userProfilePic = text_data_json["userProfilePic"]
        col = text_data_json["col"]
        cellId = text_data_json["cellId"]
        
        #obj_user = await get_user_object(email)
        #user_profile_pic = getattr(obj_user, "profile_pic")

        if message:
            msg_id = generate_random_string(10)

            # Use database_sync_to_async to execute the create operation asynchronously
            await create_new_message(msg_id, cellId, username, email, message, col)
                
        
            await self.channel_layer.group_send(
                self.roomGroupName,{
                    "type" : "sendMessage" ,
                    "email":email,
                    "username":username ,
                    "userProfilePic":userProfilePic,
                    "message":message ,
                    "col":col ,
                    "cellId":cellId
                })
        
        
    async def sendMessage(self , event) : 
        user_ = self.scope.get('user')
        email = event["email"]
        userProfilePic = event["userProfilePic"]
        message = event["message"]


        obj_user = await get_user_object(email)
        user_profile_pic = getattr(obj_user, "profile_pic")
        if message:
            await self.send(text_data = json.dumps({
                                                    "email":email,
                                                    "userProfilePic":userProfilePic,
                                                    "message":message }))