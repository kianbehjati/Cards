from .views import *
from django.urls import path

app_name = "authentication"
urlpatterns = [
    path("login",login_view,name='login'),
    path("singup",signup_view,name='signup'),
    path("user-edit",userEdit,name='useredit'),
    path("logout",log_out,name="logout"),
    path("forget-password",forget_password,name="forgetpass"),
    path("password-change/<token>",pass_change),
    path("user-panel",user_panel,name="userpanel"),
    path("api/v1/users",UserLookUp),
    path("card-call/<user_id>",create_card_call)

]