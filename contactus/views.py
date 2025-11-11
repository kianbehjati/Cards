from django.shortcuts import render
from .forms import Contact_form
from .models import Contact
from django.views.generic.edit import FormView
from django.shortcuts import resolve_url


def contact(request):
    contact_r =  Contact_form(request.POST or None)
    context = {
        "form":contact_r,
        "status":None
    }
    if contact_r.is_valid():
        title = contact_r.cleaned_data["title"]
        text = contact_r.cleaned_data["text"]
        email = contact_r.cleaned_data["email"]
        Contact.objects.create(title=title,text=text,email=email)
        context["form_status"] = "sent"
        return render(request,"contact.html",context)
    return render(request, "contact.html", context)