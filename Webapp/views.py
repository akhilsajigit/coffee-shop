from django.shortcuts import render, redirect
from Backend.models import Category, Product
from Webapp.models import UserRegister, Cart, Order, Contact
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
import razorpay
import os


def home_page(request):
    cat = Category.objects.all()
    return render(request, "home.html", {'cat': cat})


def about_page(request):
    cat = Category.objects.all()
    return render(request, "about.html", {'cat': cat})


def contact_page(request):
    cat = Category.objects.all()
    return render(request, "contact.html", {'cat': cat})


def service_page(request):
    cat = Category.objects.all()
    return render(request, "services.html", {'cat': cat})


def blog_page(request):
    cat = Category.objects.all()
    pdata = Product.objects.all()
    return render(request, "blog.html", {'cat': cat, 'pdata': pdata})


def shop_page(request):
    cat = Category.objects.all()
    pdata = Product.objects.all()
    return render(request, "shop.html", {'cat': cat, 'pdata': pdata})


def product_filtered(request, cat_name):
    cat = Category.objects.all()
    data = Product.objects.filter(pd_category=cat_name)
    return render(request, "product-filtered.html", {'data': data, 'cat': cat})


def single_product_page(request, p_id):
    cat = Category.objects.all()
    pdata = Product.objects.get(id=p_id)
    return render(request, "single-product.html", {'pdata': pdata, 'cat': cat})


def user_register_page(request):
    return render(request, "user-register.html")


def user_login_page(request):
    return render(request, "user-login.html")


def save_user_register(request):
    if request.method == "POST":
        una = request.POST.get('username')
        uem = request.POST.get('email_id')
        upd = request.POST.get('password')
        obj = UserRegister(user_name=una, user_email=uem, user_password=upd)
        obj.save()
        messages.success(request, "User Registered")
        return redirect(user_login_page)


def user_login_session(request):
    if request.method == "POST":
        lun = request.POST.get('uname')
        lpd = request.POST.get('pwd')
        if UserRegister.objects.filter(user_name=lun, user_password=lpd).exists():
            request.session['Username'] = lun
            request.session['Password'] = lpd
            messages.success(request, "Login Successfully")
            return redirect(home_page)
        else:
            return redirect(user_login_page)
    else:
        return redirect(user_login_page)


def user_logout(request):
    del request.session['Username']
    del request.session['Password']
    messages.success(request, "Successfully Logout")
    return redirect(home_page)


def cart_data_save(request, c_id):
    if request.method == "POST":
        try:
            c_img = request.FILES['cart_image']
            fs = FileSystemStorage()
            file = fs.save(c_img.name, c_img)
        except MultiValueDictKeyError:
            file = Product.objects.get(id=c_id).product_image
        cpn = request.POST.get('product_name')
        csn = request.POST.get('session_name')
        cqn = request.POST.get('quantity')
        c_tot = request.POST.get('total')
        obj = Cart(ct_user=csn, ct_product_name=cpn, ct_quantity=cqn, ct_total_price=c_tot,
                   ct_image=file)
        obj.save()
        messages.success(request, "Added to cart")
    return redirect(cart_page)


def delete_cart_data(request, c_id):
    x = Cart.objects.filter(id=c_id)
    x.delete()
    messages.error(request, "Deleted from cart")
    return redirect(cart_page)


def cart_page(request):
    cat = Category.objects.all()
    cart_data = Cart.objects.filter(ct_user=request.session['Username'])
    sub_total = total = delivery_charge = 0
    for i in cart_data:
        sub_total = sub_total + i.ct_total_price
        if sub_total >= 500:
            delivery_charge = 50
        else:
            delivery_charge = 100
        total = sub_total + delivery_charge
    return render(request, "cart.html", {'cat': cat, 'cart_data': cart_data, 'sub_total': sub_total,
                                         'delivery_charge': delivery_charge, 'total': total})


def checkout_page(request):
    cat = Category.objects.all()
    cart_data = Cart.objects.filter(ct_user=request.session['Username'])
    sub_total = total = delivery_charge = 0
    for i in cart_data:
        sub_total = sub_total + i.ct_total_price
    if sub_total >= 500:
        delivery_charge = 50
    else:
        delivery_charge = 100
    total = sub_total + delivery_charge
    return render(request, "check-out.html", {'cat': cat, 'cart_data': cart_data,
                                              'total': total, 'sub_total': sub_total,
                                              'delivery_charge': delivery_charge})


def save_customer_data(request):
    if request.method == "POST":
        cname = request.POST.get('customer_name')
        c_cy = request.POST.get('customer_country')
        c_add = request.POST.get('customer_address')
        c_city = request.POST.get('customer_city')
        c_em = request.POST.get('customer_email')
        pp = request.POST.get('price')
        obj = Order(customer_name=cname, customer_state=c_cy, customer_address=c_add,
                    customer_city=c_city, customer_email=c_em, order_price=pp)
        obj.save()
    return redirect(payment_page)


def payment_page(request):
    customer = Order.objects.order_by('-id').first()
    name = customer.customer_name
    pay = customer.order_price
    amount = int(pay * 100)
    pay_str = str(amount)
    if request.method == "POST":
        order_currency = "INR"
        client = razorpay.Client(auth=(os.getenv('RAZOR_KEY_ID'), os.getenv('RAZOR_KEY')))
        payment = client.order.create({'amount': amount, 'currency': order_currency, 'payment_capture': '1'})
    return render(request, "payment.html", {'name': name, 'pay_str': pay_str})


def save_feedback_data(request):
    if request.method == "POST":
        f_name = request.POST.get('f_name')
        f_mob = request.POST.get('f_mob')
        f_em = request.POST.get('f_em')
        f_sub = request.POST.get('f_sub')
        f_msg = request.POST.get('f_msg')
        obj = Contact(fd_back_name=f_name, fd_back_mobile=f_mob, fd_back_email=f_em,
                      fd_back_subject=f_sub, fd_back_message=f_msg)
        obj.save()
        return redirect(contact_page)
