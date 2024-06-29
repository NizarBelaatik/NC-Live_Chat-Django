from django.contrib import admin
from .models import USER
from .models import Chats_BOX, chat_msg ,chat_file
# Register your models here.
admin.site.register(USER)
admin.site.register(Chats_BOX)
admin.site.register(chat_msg)
admin.site.register(chat_file)