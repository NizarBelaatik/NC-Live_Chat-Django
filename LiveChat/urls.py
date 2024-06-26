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
from LiveChat_app.views import HOME
from LiveChat_app.views import  LoginU,Login, SignUP,SignupU 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', Login, name="login"),
    path('LoginU/', LoginU, name="LoginU"),
    path('signup/', SignUP ,name="signup"),
    path('SignupU/', SignupU ,name="SignupU"),

    path('home/', HOME ,name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)