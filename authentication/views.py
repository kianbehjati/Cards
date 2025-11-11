from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, resolve_url
from rest_framework.decorators import api_view
from card.models import Card
from .forms import *
from .models import myUser,Temp_Token
from django.http import *
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.conf import settings
import datetime


def is_auth(request) -> bool:
    return request.user.is_authenticated

def pass_validate(pass1,pass2):
    if pass1 == pass2:

        if len(pass1) < 8:
            return "your password should be at least 8 char length"
        else:
            chars = "QWERTYUIOPASDFGHJKLZXCVBNM"
            nums = "1234567890"
            specials = "!@#$%^&*"

            is_upper = False
            is_lower = False
            is_special_char = False
            is_num = False

            for char in pass1:
                if char in chars:
                    is_upper = True
                elif char in chars.lower():
                    is_lower = True
                elif char in nums:
                    is_num = True
                elif char in specials:
                    is_special_char = True
                else:
                    continue

            if is_upper and is_lower and is_num and is_special_char:
                return True
            else:
                return "please use A-Z, a-z , 0-9 and sepcial characters(!@#$%^&*) in your password"


    else:
        return "please confirm password correctly"


def login_view(request):

    if not is_auth(request):
        log_form = login_form(request.POST or None)
        context = {
            "form": log_form
        }
        if log_form.is_valid():
            username = log_form.cleaned_data["user_name"]
            password = log_form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user is None:
                log_form.add_error(field=None,error="wrong credintials")
                return render(request, "login.html", context)
            else:
                login(request,user)
                try:
                    if request.GET["next"] != resolve_url("authentication:login"):
                        return redirect(request.GET["next"])
                    else:
                        return render(request,"login.html",context)
                except:
                    return redirect("authentication:userpanel")

        return render(request,"login.html",context)

    else:

        return redirect(f'/auth/logout?next={resolve_url("authentication:login")}')

@login_required(login_url="/auth/login")
def log_out(request):
    logout(request)
    try:
        return redirect(request.GET['next'])
    except:
        return redirect('/')

@login_required(login_url='/auth/login')
def user_panel(request):

    context = {
        "card":None
    }

    card = Card.objects.filter(owner_id=request.user.id)
    if card.exists():
        context["card"] = card.first()
        return render(request,"user_panel.html",context)
    else:
        return render(request, "user_panel.html", context)


@login_required(login_url='/auth/login')
def userEdit(request):

    context = {
        "err":None
    }

    if request.POST:

        username = request.POST.get('user_name')
        email = request.POST.get('email')
        phone_number = request.POST.get("phone_input").replace(" ","")

        if username and (email or email == "") and phone_number:

            username_changed = not (username == request.user.username)
            email_changed = not (email == request.user.email)
            phone_number_changed = not (phone_number == request.user.phone_number)



            if username_changed and email_changed and phone_number_changed:
                if myUser.objects.filter(username=username).exists():
                    context["err"] = "an other user use same User name"
                    return render(request, 'user-edit.html', context)
                if myUser.objects.filter(email=email).exists():
                    context["err"] = "an other user use same Email"
                    return render(request, 'user-edit.html', context)
                if myUser.objects.filter(phone_number=phone_number).exists():
                    context["err"] = "an other user use same Phone Number"
                    return render(request, 'user-edit.html', context)

                user = myUser.objects.get(id=request.user.id)
                user.username = username
                user.email = email
                user.phone_number = phone_number
                user.save()

                return redirect(resolve_url("authentication:userpanel"))

            if username_changed and email_changed:
                if myUser.objects.filter(username=username).exists():
                    context["err"] = "an other user use same User name"
                    return render(request, 'user-edit.html', context)
                if myUser.objects.filter(email=email).exists():
                    context["err"] = "an other user use same Email"
                    return render(request, 'user-edit.html', context)
                user = myUser.objects.get(id=request.user.id)
                user.username = username
                user.email = email
                user.save()
                return redirect(resolve_url("authentication:userpanel"))

            elif username_changed and phone_number_changed:
                if myUser.objects.filter(username=username).exists():
                    context["err"] = "an other user use same User name"
                    return render(request, 'user-edit.html', context)
                if myUser.objects.filter(phone_number=phone_number).exists():
                    context["err"] = "an other user use same Phone Number"
                    return render(request, 'user-edit.html', context)
                user = myUser.objects.get(id=request.user.id)
                user.username = username
                user.phone_number = phone_number
                user.save()
                return redirect(resolve_url("authentication:userpanel"))

            elif email_changed and phone_number_changed:
                if myUser.objects.filter(phone_number=phone_number).exists():
                    context["err"] = "an other user use same Phone Number"
                    return render(request, 'user-edit.html', context)
                if myUser.objects.filter(email=email).exists():
                    context["err"] = "an other user use same Email"
                    return render(request, 'user-edit.html', context)
                user = myUser.objects.get(id=request.user.id)
                user.email = email
                user.phone_number = phone_number
                user.save()
                return redirect(resolve_url("authentication:userpanel"))

            elif username_changed:
                if myUser.objects.filter(username=username).exists():
                    context["err"] = "an other user use same User name"
                    return render(request, 'user-edit.html', context)
                user = myUser.objects.get(id=request.user.id)
                user.username = username
                user.save()
                return redirect(resolve_url("authentication:userpanel"))

            elif email_changed:
                if email == "":
                    print('h')
                    user = myUser.objects.get(id=request.user.id)
                    user.email = email
                    user.save()
                    return redirect(resolve_url("authentication:userpanel"))
                else:
                    if myUser.objects.filter(email=email).exists():
                        context["err"] = "an other user use same Email"
                        return render(request, 'user-edit.html', context)
                    user = myUser.objects.get(id=request.user.id)
                    user.email = email
                    user.save()
                    return redirect(resolve_url("authentication:userpanel"))

            elif phone_number_changed:
                if myUser.objects.filter(phone_number=phone_number).exists():
                    context["err"] = "an other user use same Phone Number"
                    return render(request, 'user-edit.html', context)
                user = myUser.objects.get(id=request.user.id)
                user.phone_number = phone_number
                user.save()
                return redirect(resolve_url("authentication:userpanel"))
            else:
                return redirect(resolve_url("authentication:userpanel"))

        else:
            return render(request, 'user-edit.html', context)

    return render(request,'user-edit.html',context)

def signup_view(request):
    if not is_auth(request):
        signup_for = signup_form(request.POST or None)

        context = {
            "form": signup_for
        }

        if signup_for.is_valid():

            username = signup_for.cleaned_data['user_name']
            email = signup_for.cleaned_data['email']
            phone_number = request.POST.get('phone_input')
            password = signup_for.cleaned_data['password']
            confirm_password = signup_for.cleaned_data['confirm_password']

            if type(pass_validate(password,confirm_password)) == str:
                signup_for.add_error(field=None,error=pass_validate(password,confirm_password))
                return render(request, 'register.html', context=context)

            else:
                user = myUser.objects.filter(Q(username=username) | Q(phone_number=phone_number.replace(" ","")) | Q(email=email))

                if phone_number == "":
                    signup_for.add_error(field=None, error="you should enter a phone number")
                    return render(request, 'register.html', context=context)

                if len(phone_number) > 14:
                    signup_for.add_error(field=None, error="something is wrong with your phone number")
                    return render(request, 'register.html', context=context)

                if user:
                    if myUser.objects.filter(username=username).exists():
                        signup_for.add_error(field=None, error="an other user uses same username")
                        return render(request, 'register.html', context=context)
                    if email != "":
                        if myUser.objects.filter(email=email).exists():
                            signup_for.add_error(field=None, error="an other user use same email")
                            return render(request, 'register.html', context=context)

                    if myUser.objects.filter(phone_number=phone_number.replace(" ","")).exists():
                        signup_for.add_error(field=None, error="an other user use same phone number")
                        return render(request, 'register.html', context=context)

                else:
                    if email == "" :
                        myUser.objects.create_user(username=username,phone_number=phone_number,password=password)
                        user = authenticate(username=username, password=password)
                        login(request, user)
                        return redirect(resolve_url('authentication:userpanel'))

                    else:
                        myUser.objects.create_user(username=username, phone_number=phone_number, email=email, password=password)
                        user = authenticate(username=username, password=password)
                        login(request,user)

                        send_mail(
                            subject="Congrats new member",
                            message=f"Hi dear {user.username} \n we wish you best experience \n\n درود {user.username} به وبسایت من خوش امدید و بهترین تجربه رو برای شما ارزومند هستم",
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[user.email],
                            fail_silently=True
                        )
                        return redirect(resolve_url('authentication:userpanel'))
    else:
        return redirect(f'/auth/logout?next={resolve_url("authentication:signup")}')


    return render(request,'register.html',context=context)


def forget_password(request):

    fp_form = Forget_pass(request.POST or None)
    context = {
        "form":fp_form
    }
    if fp_form.is_valid():
        username = fp_form.cleaned_data["username"]
        phone_nhumber = fp_form.cleaned_data["phone_number"]


        user = myUser.objects.filter(username=username,phone_number=phone_nhumber)

        if user.exists():
            user = user.first()
            # try:
            token = user.temp_token_set.create()
            return redirect(f'/auth/password-change/{token.token}')
            # except:
            #     token = Temp_Token.objects.get(user_id=user.id)
            #     token.delete()
            #     token = Temp_Token.objects.create(user_id=user.id)
            #     return redirect(f'/auth/password-change/{token.token}')
        else:
            fp_form.add_error(field=None,error="wrong credintials")
            return render(request,"forget_password.html",context)

    return render(request,"forget_password.html",context)


def pass_change(request,token):

    token = Temp_Token.objects.filter(token=token,is_valid=True)

    change_form = Change_pass(request.POST or None)

    context = {
        "form":change_form
    }

    if token.exists():

        today = datetime.datetime.today().replace(tzinfo=None)

        delta = today - token.first().created_date.replace(tzinfo=None)

        token = token.first()

        seconds = delta.seconds - 12600

        if delta.days == 0 and seconds < 300: #after 5 minutes token'll be devalidated

            if change_form.is_valid():

                password = change_form.cleaned_data["password"]
                confirm_passowrd = change_form.cleaned_data["confirm_password"]

                if type(pass_validate(password,confirm_passowrd)) == bool:

                    user = myUser.objects.filter(temp_token=token)


                    if user.exists():
                        user = user.first()
                        user.set_password(password)
                        user.save()

                        token.is_valid = False
                        token.save()

                        return redirect("authentication:login")

                    else:
                        return render(request, 'password_change.html', context=context)

                else:

                    change_form.add_error(field=None, error=pass_validate(password,confirm_passowrd))
                    return render(request, 'password_change.html', context=context)

        else:
            
            token.is_valid = False
            token.save()
            return HttpResponseBadRequest()


    else:
        return HttpResponseBadRequest('')

    return render(request, 'password_change.html', context=context)


def create_card_call(request,user_id):
    card = Card.objects.filter(owner=user_id)
    if not card.exists():

        Card.objects.create(owner_id=user_id,balance=1000,secret_key="hi")

        return redirect(resolve_url("authentication:userpanel"))

    else:
        return HttpResponseBadRequest()


####################### api #######################


@api_view(["POST"])
def UserLookUp(request):

    get_user = myUser.objects.filter(username=request.data['username'])

    if get_user:

        if get_user.first().check_password(request.data['password']):
            return JsonResponse(list(get_user.values("id","username","phone_number","email"))[0],safe=False)

        else :
            return HttpResponseNotFound("User not found")
