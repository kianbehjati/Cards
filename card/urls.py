from django.urls import path
from .views import *

urlpatterns = [
    path('pay-factor/<paylink>',pay_factor,name="payfactor"),
    path('transactions/<card_number>',transactions,name="trainsactions"),
    path('transfer',transfer,name="transfer"),
    path("api/v1/factor-list",payfactor_list.as_view()),
    path("api/v1/factor",create_factor),
    path("card-create",Cardcreate.as_view(),name="create_card"),
    path("api/v1/card/<card_number>",lookUp_card)
]