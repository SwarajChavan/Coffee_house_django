from django.shortcuts import render, redirect
from django.http import HttpResponse
from.models import *
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        username=request.user.username
        items=Items.objects.all().order_by('price')
        order_item= OrderItem.objects.filter(user= request.user, ordered= False).order_by('item__price')
        len_oi= len(order_item)
        return render(request,'home.html',{'items':items, 'len_oi': len_oi})
    else:
        items=Items.objects.all().order_by('price')
        return render(request, 'home.html', {'items':items})

def about_us(request):
    return render(request,'About.html')