from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone



# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class USER(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    num = models.CharField(max_length=30, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    profile_pic = models.ImageField(blank=True, upload_to='uploads/profilepic', null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    user_id = models.CharField(max_length=255,blank=True, null=True)
    


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname','lastname']

    def __str__(self):
        return self.email
    

class chats(models.Model):
    chat_box_id = models.CharField(max_length=30, blank=True, null=True) # convertion id
    title = models.CharField(max_length=100, blank=True, null=True)
    chats_users = models.TextField(blank=True)
    img = models.ImageField(blank=True, upload_to='uploads/chats_img', null=True)
    grp = models.BooleanField(default=False)
    last_msg = models.TextField(blank=True)
    last_msg_time = models.DateTimeField(blank=True, null=True)
    
    def chats_users_as_list(self):
        return self.chats_users.split(' ')
    
class chat_msg(models.Model):
    chat_msg_id = models.CharField(max_length=30, blank=True, null=True) # 
    chat_box_id = models.CharField(max_length=30, blank=True, null=True) # convertion id
    user = models.CharField(max_length=30, blank=True, null=True) # email
    chat_date = models.DateTimeField(default=timezone.now)

    contain_txt = models.BooleanField(default=False)
    chat = models.TextField()
    
    contain_file = models.BooleanField(default=False)
    file_type = models.CharField(max_length=30, blank=True, null=True)
    file = models.ImageField(blank=True, upload_to='uploads/chat_files', null=True)
    
    contain_files = models.BooleanField(default=False)
    files_id = models.CharField(max_length=30, blank=True, null=True)

class chat_file(models.Model):
    chat_file_id = models.CharField(max_length=30, blank=True, null=True)
    files_id = models.CharField(max_length=30, blank=True, null=True)
    file = models.ImageField(blank=True, upload_to='uploads/chat_files', null=True)
    file_type = models.CharField(max_length=30, blank=True, null=True)