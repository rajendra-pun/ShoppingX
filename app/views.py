from django.shortcuts import redirect, render
# impoiting View for making class based view
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# login required for function base view
from django.contrib.auth.decorators import login_required
# login required for class base view
from django.utils.decorators import method_decorator


# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        # if we have selected product already then direct show go to cart button on product detail page otherwise show add to cart button
        # if product item already selected, cartma same item xa bhne false
        item_already_in_cart = False
        # if cartma product xaina bhne show add to cart button on detail page of product, also check product id and loggedin user
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        # return render(request, 'app/productdetail.html',  {'product':product})
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect ('/cart')

# ushko cart matra show garnu jasle login garekoxa aruko cart not to show
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        # for calculating product quantity plus, minus and total money calculating, etc
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0 
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        # if there is product in cart
        if cart_product:
            for p in cart_product:
                tempamount =(p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
        # when cart is empty, when there are no products then show empty cart page
        else:
            return render(request, 'app/emptycart.html')

# we get data in this function from javascript plus, minus, remove
def plus_cart(request):
    if request.method == 'GET':
        # we get prod id from javascript ajax
        prod_id = request.GET['prod_id']
        print(prod_id)
        print('prodct id clicked')
        
        # now verify which user is loged in clicking the button and etc
        # c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()

        # now again recalculating and showing total amount
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            # 'totalamount': totalamount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        # we get prod id from javascript ajax
        prod_id = request.GET['prod_id']
        # now verify which user is loged in clicking the button and etc
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1;
        c.save()

        # now again recalculating and showing total amount
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount
        
        data={
            'amount':amount,
            'totalamount':amount + shipping_amount
        }

        return JsonResponse(data)

def buy_now(request):
      return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Samsung' or data == 'Iphone' or data == 'Oppo':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    # show mobile price less than 10,000, 
    # lt = less then
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=1000)
    # show mobile price greater than 10,000
    # gt = greater than
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=1000)

    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def topwear(request, topweardata=None):
    if topweardata == None:
        tshirt = Product.objects.filter(category='TW')
    elif topweardata == 'Park' or topweardata == 'Polo':
        tshirt = Product.objects.filter(category='TW').filter(brand=topweardata)
    # show tshirt only Park company name
    # elif topweardata == 'Park':
    #     tshirt = Product.objects.filter(category='TW').filter(brand='')

    return render(request, 'app/topwear.html', {'tshirt':tshirt})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    # first capture user which user is logged in or not
    user = request.user
    # getting address which user is logged in, filtering the data which user is loggedin or not
    add = Customer.objects.filter(user=user)
    # showing which products are in carts in checkout page, also check which user is loggedin
    cart_items = Cart.objects.filter(user=user)

    # now showing total amount of cart items in checkout page
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    # if cartma product xa bhne then will run for loop
    if cart_product:
        for p in cart_product:
            temamount = (p.quantity * p.product.discounted_price) 
            amount += temamount
        totalamount = amount + shipping_amount
    
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items': cart_items})

@login_required
def payment_done(request):
    user = request.user
    # getting customer id using name in radio button in checkout html name="custid", value ad.id xa tyo eta custidma auxa
    custid = request.GET.get('custid')
    # now filter customer id
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    # we need product which are selected in cart page 
    ''' direct cartma dherai users haruley select gareko product huna sakxa
    so now jun loggedin user xa ushle matra select gareko product filter garerw dekhauxa '''
    cart = Cart.objects.filter(user=user)
    # for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    # payment donema product display hunxa and only cartma vako product delete hunxa but order placema vako product delete hudaina you can check in admin panel
    c.delete()
    return redirect('orders')


# @method_decorator(login_required, name='dispatch')
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')

        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
            
