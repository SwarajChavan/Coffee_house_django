from django.urls import path
from.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register',register,name="register"),
    path('login', Login, name='login'),
    path('logout',Logout, name='logout'),
    path('<pk>/update-profile/', UsersUpdateView.as_view(), name = 'update-profile'),
    path('orders/', OrdersListView.as_view(), name='orders-list'),
    path('change-password/', ChangePasswordView.as_view(), name = 'change-password'),
    ]