from django.shortcuts import redirect,render,get_object_or_404,HttpResponse,HttpResponseRedirect
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
import json
from django.contrib import messages
from .models import Item, Order 
from .forms import ItemForm, SignupForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from guest_user.decorators import allow_guest_user
import requests
from django.middleware.csrf import get_token

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
YOUR_DOMAIN = 'http://localhost:8000'

def home(request):
    products = Item.objects.all()
    form1 = SignupForm()
    if request.method=="POST":
        if 'signup' in request.POST:
            form1=SignupForm(request.POST)
            if form1.is_valid():
                user=form1.save(commit=False)
                user.is_active=True
                user.save()
                return redirect('home')
        elif 'login' in request.POST:
            u_email = request.POST['email']
            u_password = request.POST['password']
            user = authenticate(request, email=u_email, password=u_password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('home')
    else:
        return render(request,"home.html", {"products": products,"form1": form1})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request):
    user = request.user
    ### boring user details modifications ...
    orders = Order.objects.filter(user=request.user, payed=True)
    return render(request,"profile.html", {"orders": orders})
    
def refund(request):
    data = json.loads(request.body)
    try:
        refund = stripe.Refund.create(data['pi'])
        return JsonResponse({"message":"success"})
    except Exception as e:
        return JsonResponse({'error': (e.args[0])}, status =403)
        

@login_required
def plan(request):
    # Plan is for practice only.
    if request.method=="POST":
        data = json.loads(request.body)
        product = stripe.Product.retrieve(data['id'])
        price = stripe.Price.list(product=product)
        custm_check = stripe.Customer.list(email=data['email'])
        if not custm_check:
            try:
                customer = stripe.Customer.create(
                    email=data["email"],
                )
                payment = stripe.checkout.Session.create(
                    customer=customer.id,
                    line_items=[
                        {
                            'price': price.data[0].id,
                            'quantity': 1,
                        },
                    ],
                    metadata={"email":data['email']},
                    mode='subscription',
                    ui_mode = 'embedded',
                    # payment_method_types=['paypal'],
                    return_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                )
                stripe.Customer.modify(
                  customer.id,
                  metadata={"price": price.data[0].id},
                )
                return JsonResponse({"clientSecret":payment.client_secret})
            except Exception as e:
                return JsonResponse({'error': (e.args[0])}, status =403)
        elif custm_check.data[0]["metadata"]["price"]==price.data[0].id:
            return redirect('plan')
        else:
            try:
                subscription = stripe.Subscription.list(customer=custm_check.data[0].id)
                stripe.Subscription.cancel(subscription.data[0].id)
                stripe.Customer.modify(
                  custm_check.data[0].id,
                  metadata={"price": price.data[0].id},
                )
                payment = stripe.checkout.Session.create(
                    customer=custm_check.data[0].id,
                    line_items=[
                        {
                            'price': price.data[0].id,
                            'quantity': 1,
                        },
                    ],
                    metadata={"email":data['email']},
                    mode='subscription',
                    ui_mode = 'embedded',
                    # payment_method_types=['paypal'],
                    return_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
                )
                return JsonResponse({"clientSecret":payment.client_secret})
            except Exception as e:
                return JsonResponse({'error': (e.args[0])}, status =403)            
    else:
        filters={'type': 'service','active': True,}
        products = stripe.Product.list(**filters)
        prod_ids=[prod["id"] for prod in products]
        prices = [stripe.Price.list(product = prod).data for prod in prod_ids]
        for i in range(len(prod_ids)):
            products["data"][i]["price_id"]=prices[i][0]["id"]
            products["data"][i]["amount"]=prices[i][0]["unit_amount"]/100
            products["data"][i]["currency"]=prices[i][0]["currency"]
        return render(request,"plan.html",{"products": products})

@staff_member_required
def create_prod(request):
    if request.method=='POST':
        data = request.POST
        form=ItemForm(data,request.FILES)
        if form.is_valid():
            try:    
                product = stripe.Product.create(
                    name=data.get('name'),
                    description=data.get('description'),
                    type="good",
                )
                stripe.Price.create(
                    currency="usd",
                    unit_amount=int(float(data.get('price'))*100),
                    product=product.id,
                    metadata={
                    },
                )
                item = form.save(commit=False)
                item.stripe_id = product.id
                item.save()
                return redirect('detail-prod',id=item.id)
            except Exception as e:
                return JsonResponse({'error': (e.args[0])}, status =403)
    else:
        form=ItemForm()
    return render(request,'create_prod.html',{'form':form})

@staff_member_required
def delete(request,id):
    item=get_object_or_404(Item,pk=id)
    try:    
        product = stripe.Product.modify(
            item.stripe_id,
            active=False,
        )
        prod=stripe.Price.list(product=item.stripe_id)
        stripe.Price.modify(
            prod.data[0].id,
            active=False,
        )
    except Exception as e:
        return JsonResponse({'error': (e.args[0])}, status =403)
    item.delete()
    return redirect('home')

@staff_member_required
def edit(request,id):
    item=get_object_or_404(Item,pk=id)
    if request.method=='POST':
        data = request.POST
        form=ItemForm(data,request.FILES,instance=item)
        if form.is_valid():
            try:    
                product = stripe.Product.modify(
                    item.stripe_id,
                    name=data.get('name'),
                    description=data.get('description'),
                )
                stripe.Price.modify(
                    stripe.Price.list(product=item.stripe_id).id,
                    unit_amount=int(float(data.get('price'))*100),
                )
                form.save()
                return redirect('detail',id=form.id)
            except Exception as e:
                return JsonResponse({'error': (e.args[0])}, status =403)
    else:
        form=ItemForm(instance=item)
    return render(request,'create_prod.html',{'form':form})

@allow_guest_user
def detail(request,id):
    item=get_object_or_404(Item,pk=id)
    related_items=Item.objects.filter(category=item.category).exclude(pk=id)[0:3]
    return render(request,'detail-prod.html',{
       'item':item,
       'related_items':related_items,
    })

@allow_guest_user
def cart(request):
    orders = Order.objects.filter(user=request.user, payed=False)
    return render(request, "cart.html", {"orders": orders})

@allow_guest_user
def add_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        existing_order = Order.objects.filter(user=request.user, item=item).first()
        if existing_order:
            return JsonResponse({'message': 'This item is already in your cart.'})
        order = Order.objects.create(user=request.user, item=item)
        order.save()
        return JsonResponse({'message': 'Item added to cart successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
        
@allow_guest_user
def quantity_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        if data.get('action')=="increase":
            order.quantity+=1
            order.save()
        elif data.get('action')=="decrease":
            if order.quantity>1:
                order.quantity-=1
                order.save()
        return JsonResponse({'quantity': order.quantity})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@allow_guest_user
@csrf_exempt
def delete_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get("payed"):
            data.pop("payed")
            pi = data.pop("pi_id")
            for order in data.values():
                order = get_object_or_404(Order, pk=order)
                order.payed = True
                order.pi = pi
                order.save()
        else:
            for key,order in data.values():
                order = get_object_or_404(Order, pk=order)
                order.delete()
        return JsonResponse({'message': 'Item deleted from cart successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@allow_guest_user
def purchase_int(request):
    data = json.loads(request.body)
    data_items=[
      {
          'price': stripe.Price.list(product=stripe.Product.retrieve(order["stripe_id"])).data[0].id,
          'quantity':order["quantity"],
      } for order in data
    ]
    meta_orders=[str(order["order_id"]) for order in data]
    try:
        payment = stripe.checkout.Session.create(
            line_items=data_items,
            metadata=meta_orders,
            ui_mode = 'embedded',
            mode='payment',
            shipping_address_collection = {
                'allowed_countries':['US','GB','DZ','ES']
            },
            shipping_options=[
                {
                  "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 0, "currency": "usd"},
                    "display_name": "Free shipping",
                    "delivery_estimate": {
                      "minimum": {"unit": "business_day", "value": 15},
                      "maximum": {"unit": "business_day", "value": 30},
                    },
                  },
                },
                {
                  "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {"amount": 999, "currency": "usd"},
                    "display_name": "DHL",
                    "delivery_estimate": {
                      "minimum": {"unit": "business_day", "value": 1},
                      "maximum": {"unit": "business_day", "value": 3},
                    },
                  },
                },
            ],
            # payment_method_types=['paypal'],
            return_url=YOUR_DOMAIN + '/success?session_id={CHECKOUT_SESSION_ID}',
        )
        return JsonResponse({"clientSecret":payment.client_secret})
    except Exception as e:
        return JsonResponse({'error': (e.args[0])}, status =403)

def session_stat(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)
    customer_email = session['customer_details']["email"]
    if session["mode"]=="payment":
        order_id = session['metadata']
        order_id["payed"]=True
        order_id["pi_id"]=session["payment_intent"]
        headers = {
            'content-type': 'application/json',
        }
        requests.post(request.build_absolute_uri(reverse('del-cart')), data=json.dumps(order_id), headers=headers)
    return JsonResponse({"customer_email": customer_email, "status": session.status})

def complete(request):
    return render(request, 'return.html')

@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse("Invalid payload",status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse("Invalid signature",status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        
        
        return HttpResponse("Checkout session completed successfully", status=200)
    else:
        return HttpResponse(f"Unhandled event type: {event['type']}", status=200)
        
def bank_crt(request):
    return render(request, "bank_create.html")
    
def bank_con(request):
    data=request.POST
    try:
        cust=stripe.Customer.create(
            name=data["name"],
            email=data["email"]
        )
        cust.create_source(
            cust.id,
            source=data['stripeToken']
        )
    except ValueError as e:
        return HttpResponse("Invalid payload",status=400)
        
    return HttpResponse("Checkout session completed successfully", status=200)
    
### in-page checkout ###

# def purchase_int(request,id):
    # try:
        # req_json = json.loads(request.body)
        # customer = stripe.Customer.create(email=req_json['email'])
        # product=stripe.Product.retrieve(id)
        # price=stripe.Price.list(product=product)
        # intent = stripe.PaymentIntent.create(
            # amount=price.data[0].unit_amount,
            # currency='usd',
            # customer=customer['id'],
            # metadata={
                # "product_id": product.id
            # }
        # )
        # return JsonResponse({
            # 'clientSecret': intent['client_secret']
        # })
    # except Exception as e:
        # return JsonResponse({ 'error': str(e) })