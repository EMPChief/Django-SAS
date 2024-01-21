import json
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages import error
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import User, Plan
from djstripe.models import Product, PaymentMethod, Customer, Subscription

from .forms import SignUpForm
from .my_dec import need_log_out

@need_log_out('home')
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'account/register.html', context)

@need_log_out('home')
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'account/login.html')

@login_required(login_url='/login/')
def custom_logout(request):
    logout(request)
    return redirect('home')

@login_required
def checkout(request):
    products = Product.objects.all()
    return render(request, "account/checkout.html", {"products": products})

@login_required
def create_sub(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = data['payment_method']
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        PaymentMethod.sync_from_stripe_data(payment_method_obj)

        try:
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={'default_payment_method': payment_method}
            )

            djstripe_customer = Customer.sync_from_stripe_data(customer)
            request.user.customer = djstripe_customer

            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": data["price_id"]}],
                expand=["latest_invoice.payment_intent"]
            )

            djstripe_subscription = Subscription.sync_from_stripe_data(subscription)
            request.user.subscription = djstripe_subscription
            subscriber_plan, _ = Plan.objects.get_or_create(name="subscriber")
            request.user.plan = subscriber_plan
            request.user.save()

            return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status=403)
    else:
        return HttpResponse('Request method not allowed')

def complete(request):
    return render(request, "account/complete.html")

def cancel(request):
    if request.user.is_authenticated:
        sub_id = request.user.subscription.id
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            stripe.Subscription.delete(sub_id)
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status=403)
    return redirect("home")
