from django.contrib import admin
from .models import USER
from .models import chats, chat_msg ,chat_file
# Register your models here.
admin.site.register(USER)
admin.site.register(chats)
admin.site.register(chat_msg)
admin.site.register(chat_file)