import uuid
from django.db import models
from authentication.models import myUser
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from core.settings import PEPPER
from hashlib import sha256
import random

class Card(models.Model):
    owner = models.ForeignKey(myUser,on_delete=models.CASCADE)
    card_number = models.CharField(max_length=36,blank=True,unique=True)
    secret_key = models.CharField(max_length=256)
    balance = models.IntegerField(blank=True,default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def set_secret(self,raw_secret):
        secret = make_secret(raw_secret)
        self.secret_key = secret

    def check_secret(self,raw_secret) -> bool:
        return self.secret_key == make_secret(raw_secret)

    def change_secret(self,raw_secret):
        self.secret_key = make_secret(raw_secret)

    def __str__(self):
        return self.owner.username


def make_secret(raw_secret) -> str:

    mixed = raw_secret + PEPPER

    hashed = sha256(mixed
                    .encode()).hexdigest()
    return hashed

@receiver(pre_save, sender=Card)
def card_handler(instance,sender,**kwargs):
    if instance.card_number == "" :
        instance.card_number = uuid.uuid4()
    if len(instance.secret_key) < 64: # if secret is hashed len is 64
        instance.secret_key = make_secret(instance.secret_key)


class Factor(models.Model):

    STATUS = [
        ("N", 'not paid'),
        ("P", 'paid')

    ]
    
    to = models.ForeignKey(Card,on_delete=models.CASCADE)
    from_u = models.ForeignKey(Card,on_delete=models.CASCADE,null=True,blank=True,related_name="from_u")
    description = models.CharField(max_length=500,null=True,blank=True)
    amount = models.IntegerField()
    status = models.CharField(default="N",max_length=500,choices=STATUS)
    pay_link = models.CharField(blank=True,max_length=500)
    payed_date = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return self.to.owner.username

@receiver(pre_save, sender=Factor)
def factor_handler(instance,sender,**kwargs):
    if instance.pay_link == "":
        CHARS = '1234567890-sdfghjkl$zxcvbnm'
        for i in random.choices(CHARS,k=64):
            instance.pay_link += i
