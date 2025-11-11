from django.contrib import admin
from .models import Contact
class Contact_Admin(admin.ModelAdmin):
    list_display = ["title","is_read","is_answered"]
    list_editable = ["is_read","is_answered"]

admin.site.register(Contact,Contact_Admin)