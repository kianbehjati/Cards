import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import pre_save
from django.dispatch import receiver


class myUserManager(BaseUserManager):
    def create_superuser(self,username,phone_number,password,email=None):

        if not phone_number:
            raise ValueError("phone number is required")

        user = self.model(
            username=username,
            phone_number = phone_number,
            email = self.normalize_email(email),
            is_superuser = True,
            is_staff = True
        )
        user.set_password(password)
        user.save()

    def create_user(self,username,phone_number,password,email=None):
        if not phone_number:
            raise ValueError("phone number is required")
        if email:
            user = self.model(
                username=username,
                phone_number = phone_number,
                email = self.normalize_email(email)
            )
            user.set_password(password)
            user.save()
        else:
            user = self.model(
                username=username,
                phone_number=phone_number,
            )
            user.set_password(password)
            user.save()

class myUser(AbstractBaseUser):
    username = models.CharField(max_length=40,unique=True)
    phone_number = models.CharField(max_length=16,unique=True)
    email = models.EmailField(unique=True,null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['phone_number']

    objects = myUserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def has_perm(self, perm, obj=None):

        return True
    def has_module_perms(self, app_label):

        return True


class Temp_Token(models.Model):

    token = models.UUIDField(null=False)

    user = models.ForeignKey(myUser,on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)

    is_valid = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Temp Token"
        verbose_name_plural = "Temp Tokens"

    def __str__(self):
        return str(self.token)

@receiver(pre_save,sender=Temp_Token)
def token_handler(sender,instance,**kwargs):

    if instance.token == None:
        instance.token = uuid.uuid4()

@receiver(pre_save,sender=myUser)
def phone_handler(sender,instance,**kwargs):
    instance.phone_number = instance.phone_number.replace(" ","")
