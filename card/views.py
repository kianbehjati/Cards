from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, resolve_url, redirect
from rest_framework.decorators import api_view
from .forms import Transfer
from .serializer import *
from rest_framework.generics import *
from .models import *
from django.http import *
import datetime


@login_required(login_url="/auth/login")
def pay_factor(request,paylink):

    user_card = Card.objects.filter(owner_id = request.user.id)

    context = {
        "error": None,
        "payed": False
    }

    if user_card:

        user_card = user_card.first()

        obj = Factor.objects.filter(pay_link=paylink)


        if obj.exists() and user_card != obj.first().to:

            context["balance"] = user_card.balance

            factor = obj.first()

            if factor.status == "payed":
                context["payed"] = True
                context["factor"] = factor
                return render(request, "factor_pay.html", context)
            else:
                factor.status = "N"
                factor.from_u = Card.objects.get(owner_id=request.user.id)
                factor.save()
                context["factor"] = factor

                if request.method == "POST":
                    if (factor.amount*1.2/100 + factor.amount) > user_card.balance:
                        context["error"] = "balance"
                        return render(request, "factor_pay.html", context)

                    else:

                        factor.to.balance +=  factor.amount
                        factor.status = "P"
                        factor.payed_date = datetime.datetime.now()
                        user_card.balance -= factor.amount*1.2/100 + factor.amount


                        factor.save()
                        factor.to.save()
                        user_card.save()

                        context["payed"] = True

                        return render(request, "factor_pay.html", context)

            return render(request,"factor_pay.html",context)

        elif not obj.exists():
            return HttpResponseNotFound("Factor Not Found")

        elif user_card == obj.first().to:
            context["error"] = "same_card"
            return render(request, "factor_pay.html", context)

    else:
        context["error"] = "no_card"
        return render(request, "factor_pay.html", context)



@login_required(login_url="/auth/login")
def transfer(request):

    transfer_form = Transfer(request.POST or None)
    context = {
        "form": transfer_form,
        "error":None
    }

    if transfer_form.is_valid():

        card = Card.objects.filter(owner_id=request.user.id, is_active=True)

        if not card.exists():
            context["error"] = "nocard"
            return render(request, "transfer.html", context)

        to = transfer_form.cleaned_data["to"]
        amount = transfer_form.cleaned_data["amount"]
        description = transfer_form.cleaned_data["description"]
        dest_card = Card.objects.filter(card_number=to)

        if dest_card.exists():
            factor = Factor.objects.create(to=dest_card.first(),amount=amount,description=description)
            factor.save()
            return redirect(resolve_url("payfactor",factor.pay_link))
        else:
            context["error"] = "unvalid card"
            return render(request, "transfer.html", context)
    return render(request, "transfer.html", context)

@login_required(login_url="/auth/login")
def transactions(request,card_number):

    user = request.user

    card = Card.objects.filter(card_number=card_number)

    if card.exists():
        card = card.first()

        if card.owner.id == user.id:

            if not request.GET:
                factors = Factor.objects.filter((Q(from_u=card) | Q(to=card)) & Q(status="P")).order_by("-payed_date")
                return render(request, "transactions.html", context={"factors": factors})
            else:
                ### search filters ###
                if request.GET.get("kind") or request.GET.get("amount"):

                    if request.GET.get("kind") and request.GET.get("amount"):

                        amount = request.GET.get("amount")
                        kind = request.GET.get("kind")

                        if amount == "highest" and kind == "outgoing":
                            factors = Factor.objects.filter(Q(from_u=card) & Q(status="payed")).order_by(
                                "-amount")
                            return render(request, "transactions.html", context={"factors": factors})

                        elif amount == "highest" and kind == "incoming":
                            factors = Factor.objects.filter(Q(to=card) & Q(status="payed")).order_by(
                                "-amount")
                            return render(request, "transactions.html", context={"factors": factors})

                        if amount == "lowest" and kind == "outgoing":
                            factors = Factor.objects.filter(Q(from_u=card) & Q(status="payed")).order_by(
                                "amount")
                            return render(request, "transactions.html", context={"factors": factors})

                        elif amount == "lowest" and kind == "incoming":
                            factors = Factor.objects.filter(Q(to=card) & Q(status="payed")).order_by(
                                "-amount")
                            return render(request, "transactions.html", context={"factors": factors})

                        else:
                            factors = Factor.objects.filter((Q(from_u=card) | Q(to=card)) & Q(status="payed")).order_by(
                                "-payed_date")
                            return render(request, "transactions.html", context={"factors": factors})

                    else:

                        amount = request.GET.get("amount")
                        kind = request.GET.get("kind")

                        if amount:
                            if amount == "highest":
                                factors = Factor.objects.filter(
                                    (Q(from_u=card) | Q(to=card)) & Q(status="payed")).order_by("-amount")
                                return render(request, "transactions.html", context={"factors": factors})
                            elif amount == "lowest":
                                factors = Factor.objects.filter(
                                    (Q(from_u=card) | Q(to=card)) & Q(status="payed")).order_by("amount")
                                return render(request, "transactions.html", context={"factors": factors})
                            else:
                                factors = Factor.objects.filter(
                                    (Q(from_u=card) | Q(to=card)) & Q(status="payed")).order_by(
                                    "-payed_date")
                                return render(request, "transactions.html", context={"factors": factors})

                        else:
                            if kind == "incoming":
                                factors = Factor.objects.filter(
                                    Q(to=card) & Q(status="payed")).order_by("-payed_date")
                                return render(request, "transactions.html", context={"factors": factors})
                            elif kind == "outgoing":
                                factors = Factor.objects.filter(
                                    Q(from_u=card) & Q(status="payed")).order_by("-payed_date")
                                return render(request, "transactions.html", context={"factors": factors})
                            else:
                                factors = Factor.objects.filter(
                                    (Q(from_u=card) | Q(to=card)) & Q(status="payed")).order_by(
                                    "-payed_date")
                                return render(request, "transactions.html", context={"factors": factors})
                ### end of search filters ###

        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponse("You Have No Card")



##### api #####
@api_view(['POST'])
def create_factor(request):

    try:
        to = request.data["to"] #to card number
        amount = request.data["amount"]
        description = request.data["description"]


        if Card.objects.filter(card_number=to).exists():
            card = Card.objects.get(card_number=to)
            f = Factor.objects.create(to=card,description=description,amount=amount)
            f.save()
            return JsonResponse({"pay:url":resolve_url("payfactor",f.pay_link)})
        else:
            return JsonResponse(dict({"error":"card not exists"}),safe=False)
    except:
        return JsonResponse(dict({"required fields are" : "to(card_number),amount,description"}),safe=False)

@api_view(['GET'])
def lookUp_card(request,card_number):

    card = Card.objects.filter(card_number=card_number)

    if card.exists():
        card = card.first()
        return JsonResponse(dict({"username":card.owner.username}),safe=False)
    else:
        return JsonResponse(dict({"error": "user not found"}), safe=False)

class Cardcreate(CreateAPIView):

    serializer_class = card_serializer

    def perform_create(self, serializer):
        serializer.save()

class payfactor_list(ListAPIView):
    serializer_class = factor_serializer

    queryset = Factor.objects.all()
##### end api #####