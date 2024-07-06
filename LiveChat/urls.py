"""
URL configuration for LiveChat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from LiveChat_app.views import HOME ,open_chat_area,load_conv_area,load_add_conv,create_chat,load_details_area,upload_files_from_chat
from LiveChat_app.views import  LoginU,Login, SignUP,SignupU 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HOME),
    path('login/', Login, name="login"),
    path('LoginU/', LoginU, name="LoginU"),
    path('signup/', SignUP ,name="signup"),
    path('SignupU/', SignupU ,name="SignupU"),

    path('home/', HOME ,name="home"),

    path('open-conv/',open_chat_area,name="open-conv"),
    path('load-conv-area/',load_conv_area,name="load-conv-area"),
    path('add-conv/',load_add_conv,name='add-conv'),
    path('create-chat/',create_chat,name='create-chat'),
    path('load-details-area/',load_details_area,name="load-details-area"),
    path('upload-files-from-chat/',upload_files_from_chat,name="upload-files-from-chat"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)