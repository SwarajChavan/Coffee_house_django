from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from.forms import *
from django.contrib import messages
import logging, traceback
import hashlib
from random import randint
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponseNotFound
from.models import *
from Home.models import*
# from .forms import CheckoutForm

# Create your views here.
def order(request):
    if request.user.is_authenticated:
        items=Items.objects.all().order_by('price')
        order_item= OrderItem.objects.filter(user= request.user, ordered= False).order_by('item__price')
        len_oi= len(order_item)
        try:
            order = Orders.objects.get(ordered_by=request.user,ordered= False)
            return render(request,'order.html',{'items':items, 'order_item':order_item, 'len_oi':len_oi, 'order':order})
        except:
            return render(request,'order.html',{'items':items, 'order_item':order_item, 'len_oi':len_oi})

    else:
        return redirect('login')

def order_summary(request):
    order_item= OrderItem.objects.filter(user=request.user, ordered=False)
    len_oi = len(order_item)
    try:
        order = Orders.objects.get(ordered_by=request.user,ordered= False)
        return render(request, 'order_summary.html',{'order_item':order_item, 'len_oi':len_oi, 'order':order})
    except ObjectDoesNotExist:
        messages.error(request, "you don't have an order")
        return redirect('/')

def add_to_cart(request, pk):
    item = get_object_or_404(Items, pk=pk )
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_recent = Orders.objects.filter(ordered_by =request.user, ordered=False)

    if order_recent.exists():
        order = order_recent[0]

        if order.items.filter(item__pk=item.pk).exists():
            if order_item.quantity < 10:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Added quantity Item")
                return redirect("order-summary")
            else:
                return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Orders.objects.create(ordered_by=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("order-summary")

def remove_cart(request, pk):
    item= get_object_or_404(Items, pk=pk)
    order_recent= Orders.objects.filter(ordered_by= request.user, ordered=False)
    if  order_recent.exists():
        order= order_recent[0]
        if order.items.filter(item__pk= item.pk).exists():
            order_item= OrderItem.objects.filter(item= item, user= request.user, ordered=False)[0]
            order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("order-summary")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect('order-summary')
    else:
        messages.info(request, "You dont have an Order")
        return redirect('order-summary')

def reduce_quantity(request, pk):
    item= get_object_or_404(Items, pk=pk)
    order_recent= Orders.objects.filter(
        ordered_by = request.user,
        ordered = False
    )
    if order_recent.exists():
        order = order_recent[0]
        if order.items.filter(item__pk = item.pk).exists():
            order_item = OrderItem.objects.filter(
                item= item,
                user = request.user,
                ordered= False
            )[0]
            if order_item.quantity >1:
                order_item.quantity-=1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect('order-summary')
        else:
            messages.info(request,"You do not have an order")
            return redirect('order-summary')

@login_required(login_url='login')
def checkout(request):
    order_item = OrderItem.objects.filter(user=request.user, ordered=False)
    order= Orders.objects.filter(ordered_by=request.user, ordered=False)[0]
    len_oi = len(order_item)
    if request.method == 'POST':
            form = CheckoutForm(request.POST)
            if form.is_valid():
                street_name = form.cleaned_data['street_name']
                apartment_address = form.cleaned_data['apartment_address']
                city = 'Mumbai'
                pincode = int(form.cleaned_data['pincode'])
                checkout_address = str({"street": street_name, "apt_add": apartment_address, "city": city, "pin": pincode})
                update_order = Orders.objects.get(ordered_by=request.user, ordered=False)
                update_order.checkout_address = checkout_address
                update_order.save()
                return redirect(reverse('payment-gateway'))
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form,'len_oi':len_oi, 'order':order})

PAYMENT_URL_TEST = 'https://test.payu.in/_payment'
PAYMENT_URL_LIVE = 'https://secure.payu.in/_payment'
SERVICE_PROVIDER = "payu_paisa"

def payment(request):
    try:
        order= Orders.objects.filter(ordered_by=request.user, ordered=False)[0]
        if order.checkout_address !='' and order.checkout_address !=None:
            data = {}
            txnid = get_transaction_id()
            hash_ = generate_hash(request, txnid)
            hash_string = get_hash_string(request, txnid)
            payment= Payment(user=request.user, transaction_id= txnid, amount= order.get_total_price(), productinfo =  'This order is placed by '+request.user.first_name +request.user.last_name, hash = hash_, status = 'Pending', order = order)
            payment.save()
            data["action"] = PAYMENT_URL_TEST
            data["amount"] = order.get_total_price()
            data["productinfo"]  = 'This order is placed by '+request.user.first_name +request.user.last_name
            data["key"] = settings.KEY
            data["txnid"] = txnid
            data["hash"] = hash_
            data["hash_string"] = hash_string
            data["firstname"] = request.user.first_name
            data["lastname"] = request.user.last_name
            data["email"] = request.user.email
            data["phone"] = request.user.phone
            data["service_provider"] = SERVICE_PROVIDER
            data["furl"] = request.build_absolute_uri(reverse("payment-failure"))
            data["surl"] = request.build_absolute_uri(reverse("payment-success"))


            return render(request, "payu.html", {'data': data, 'order': order})
        else:
            return HttpResponseNotFound("Page Not found.")
    except:
        return HttpResponseNotFound("Page Not found.")

def generate_hash(request, txnid):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None

# create hash string using all the fields
def get_hash_string(request, txnid):
    order= Orders.objects.filter(ordered_by=request.user, ordered=False)[0]
    hash_string = settings.KEY+"|"+txnid+"|"+str(order.get_total_price())+"|"+str( 'This order is placed by '+request.user.first_name +request.user.last_name)+"|"+request.user.first_name+"|"+request.user.email+"|"+"||||||||||"+settings.SALT
    return hash_string

# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0, 99999999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().upper()[0:16]
    return txnid

@csrf_protect
@csrf_exempt
def payment_success(request):
    try:
        data = {}
        data.update(csrf(request))
        status = request.POST.get("status")
        firstname = request.POST.get("firstname")
        amount = request.POST.get("amount")
        txnid = request.POST.get("txnid")
        data_hash = request.POST.get("hash")
        key = request.POST.get("key")
        productinfo = request.POST.get("productinfo")
        email = request.POST.get("email")
        salt = settings.SALT
        try:
            additionalCharges = request.POST.get("additionalCharges")
            retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        except Exception:
            retHashSeq =salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
            hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
        if (hashh != data_hash):
             print("Invalid Transaction. Please try again")
        else:
            print("Thank You. Your order status is ", status)
            print("Your Transaction ID for this transaction is ", txnid)
            print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
            payment = Payment.objects.get(transaction_id = txnid, amount = amount, productinfo = productinfo)
            payment.status = 'Successful'
            payment.save()
            update_order = Orders.objects.get(pk = payment.order.id)
            update_order.ordered=1
            for orderitem in update_order.items.all():
                orderitem.ordered=1
                orderitem.save()
            update_order.save()
        return render(request,'payu_success.html', {'data': data, "txnid": txnid, "status": status, "amount": amount})
    except:
        return HttpResponseNotFound("Page Not Found.")

@csrf_protect
@csrf_exempt
def payment_failure(request):
    try:
        c = {}
        c.update(csrf(request))
        status = request.POST.get("status")
        firstname = request.POST.get("firstname")
        amount = request.POST.get("amount")
        txnid = request.POST.get("txnid")
        data_hash = request.POST.get("hash")
        key = request.POST.get("key")
        productinfo = request.POST.get("productinfo")
        email = request.POST.get("email")
        salt = "e5iIg1jwi8"
        try:
            additionalCharges = request.POST.get("additionalCharges")
            retHashSeq =  additionalCharges + '| '+ salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        except Exception:
            retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
        if (hashh != data_hash):
            print("Invalid Transaction. Please try again")
        else:
            print("Thank You. Your order status is ", status)
            print("Your Transaction ID for this transaction is ", txnid)
            payment = Payment.objects.get(transaction_id = txnid, amount = amount, productinfo = productinfo)
            payment.status = 'Failed'
            payment.save()
        return render(request,"payu_failure.html", {'c': c})
    except:
        return HttpResponseNotFound("Page Not Found.")
