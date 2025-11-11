from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home.as_view(),name="home"),
    path("404",view_404.as_view()),
    path('payment/',include("card.urls")),
    path('auth/',include("authentication.urls",namespace="auth")),
    path('contactus/',include("contactus.urls"))


]

urlpatterns += static(settings.STATIC_URL ,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)