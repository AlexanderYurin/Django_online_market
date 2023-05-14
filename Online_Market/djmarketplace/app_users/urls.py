from django.urls import path
from app_users.views import *

urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('', ProfileInfo.as_view(), name='profile'),
    path('logout/', logout_user, name='logout'),
    path('balance/', BalanseEdit.as_view(), name='balance'),
    path('order/', OrderView.as_view(), name='order')
]
