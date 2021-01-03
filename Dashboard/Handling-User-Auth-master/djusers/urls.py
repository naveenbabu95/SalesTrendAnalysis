from django.contrib import admin
from django.urls import path

from .views import home

from accounts.views import login_view, register_view, logout_view, admin2, index, acceptdata, viewdata

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('accounts/login/', login_view),
    path('accounts/register/', register_view),
    path('accounts/logout/', logout_view),
    path('accounts/login/admin2/', admin2),
    path('accounts/login/UserDashboard/', index),
    path('accounts/login/acceptdata/',acceptdata),
    path('accounts/login/viewdata/',viewdata)

]
