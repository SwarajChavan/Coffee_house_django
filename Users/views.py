from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import  reverse
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.views import *
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from Order.models import *
from Home.models import *
from .forms import *

# for default django auth.form
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import  authenticate, login, logout
from .models import NewUser

from.forms import *

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CustomUserCreationForm() #default django user form
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect(reverse('login'))
                messages.success(request, 'Account created successfully')
    return render(request,'register.html',{'form':form})

def Login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email= email, password= password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
        else:
            form = Customlogin(request.POST)
            return render(request, 'login.html',{'form':form})
    else:
        form = Customlogin(request.POST)
        return  render(request, 'login.html',{'form':form})

def Logout(request):
    logout(request)
    return redirect('home')


class UsersUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = 'home'
    model = NewUser
    form_class = UserUpdateForm
    template_name = 'update-profile.html'
    success_url ="/"
    def get_context_data(self, **kwargs):
            context=super().get_context_data(**kwargs)
            context['len_oi'] = len(OrderItem.objects.filter(user=self.request.user, ordered=False))
            return context

class OrdersListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'home'
    model = Payment
    template_name = 'Previous-orders.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['len_oi']= len(OrderItem.objects.filter(user=self.request.user, ordered=False))
        return context
    def get_queryset(self):
        queryset=Payment.objects.filter(user=self.request.user,status='Successful').order_by('-timestamp')
        return queryset

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    login_url = 'login'
    redirect_field_name = 'home'
    template_name = 'change-password.html'
    form_class = PasswordChangingForm
    success_url = 'login'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len_oi'] = len(OrderItem.objects.filter(user=self.request.user, ordered=False))
        return context