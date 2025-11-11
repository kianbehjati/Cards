from django.contrib import admin
from .models import Card,Factor

class Card_Admin(admin.ModelAdmin):
    class Meta:
        model = Card
    list_display = [
        'owner',
        'balance',
        'is_active'
    ]
    list_editable = ['is_active']

class Factor_Admin(admin.ModelAdmin):
    class Meta:
        model = Factor
    list_display = [
        'from_u',
        'to',
        'amount',
        'status'
    ]
    list_editable = ['status']

admin.site.register(Card,Card_Admin)
admin.site.register(Factor,Factor_Admin)