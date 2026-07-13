from django.db.models import Sum
from .models import Card,Factor
from django.shortcuts import resolve_url
from django_q.tasks import async_task
from django.conf import settings
import csv
from authentication.models import myUser
from django_q.tasks import schedule,Schedule

### monitoring & report functions ###
def total_balance():
    total = Card.objects.aggregate(Sum('balance'))
    return total["balance__sum"]

def important_users():
    users = myUser.objects.filter(card__balance__gt = 1000).values("username","phone_number","email")
    with open(f"{settings.MEDIA_ROOT}/important_users.csv","w") as f:
        writter = csv.DictWriter(f=f,fieldnames=["username","phone_number","email"])
        writter.writeheader()
        writter.writerows(list(users))
        f.close()
    return users.count()

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

### schedule(for reference) ###
# schedule('card.tasks.total_balance',schedule_type=Schedule.DAILY)
# schedule('card.tasks.important_users',schedule_type=Schedule.DAILY)
# schedule('card.tasks.unpaid_factors',schedule_type=Schedule.CRON,cron = "0 0 0/5 ? * * *") #every 5 hourd