from django.urls import path
from . views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('generate/', pageGenerator, name="pageGenerator"),
    path('qrcodes/', QRcodes, name="QRcodes")
]