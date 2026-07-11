from django.db.models import Sum
from .models import Card,Factor
from django.shortcuts import resolve_url
from django_q.tasks import async_task

### monitoring functions ###
def total_balance():
    total = Card.objects.aggregate(Sum('balance'))
    return total["balance__sum"]

def important_users():
    users = Card.objects.filter(balance__gt=1000).count()
    return users

def unpaid_factors():
    unpaid_factors = Factor.objects.filter(status="N") # cache this since it's being called multiple times
    return unpaid_factors.count()
### end monitoring ###

### notify ###
def send_unpaid_factor_notifications():
    unpaid_factors = Factor.objects.filter(status="N")

    for factor in unpaid_factors:
        owner = factor.from_u.owner
        if owner.email:
            payment_url = resolve_url("payfactor", factor.pay_link)
            message = (
                f"Hello {owner.username}, you have an unpaid factor of {factor.amount}. "
                f"Please pay it here: {payment_url}"
            )
            async_task(
                "authentication.tasks.send_email",
                owner.email,
                owner.username,
                message,
            )