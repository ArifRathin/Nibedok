from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from country.models import Country
from uuid import uuid4
import os
# Create your models here.
class UserManager(BaseUserManager):


    def create_user(self, email, first_name = "Anonymous", last_name = "User", password=None):
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, first_name="Anonymous", last_name="User", password = None):
        user = self.create_user(
            email = email,
            first_name = first_name,
            last_name = last_name,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.is_verified = True
        user.save(using = self._db)
        return user


def save_profile_photo(instance, filename):
    extension = filename.split('.')[:-1]
    if instance.pk:
        filename = f'{instance.pk}{uuid4().hex}.{extension}'
    else:
        filename = f'{uuid4().hex}.{extension}'
    upload_to = 'profile_photos'
    return os.path.join(upload_to,filename)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30, default=None, null=True)
    last_name = models.CharField(max_length=30, default=None, null=True)
    profile_photo = models.ImageField(upload_to=save_profile_photo,default='profile_photos/default.png')
    security_code = models.CharField(max_length=250, default=None, null=True)
    security_code_generated = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True)
    channel_group_name = models.CharField(max_length=250, default=None, null=True)
    websockets_opened = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=True):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def buyer_posts(self):
        return self.buyerpost_set.filter(user_id=self.id) 
    
    def latest_buyer_posts(self):
        return self.buyerpost_set.filter(user_id=self.id).order_by('-created_at')[:6]
    
    def seller_offers(self):
        return self.selleroffer_set.filter(user_id=self.id)
    
    def latest_seller_offers(self):
        return self.selleroffer_set.filter(user_id=self.id).order_by('-created_at')[:6]
    
    def post_count(self):
        return self.buyerpost_set.filter(user_id=self.id).count()
    
    def shown_prod_count(self):
        return self.selleroffer_set.filter(user_id=self.id).count()