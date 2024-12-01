from django.shortcuts import render, redirect
from Backend.models import Category, Product
from Webapp.models import Contact
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# To run index page
def index_page(request):
    C_data = Category.objects.all()
    return render(request, "index.html", {'C_data': C_data})


# To run add categories page and take input data frm user
def add_categories_page(request):
    return render(request, "add-categories.html")


# To display added Categories
def display_categories(request):
    data = Category.objects.all()
    return render(request, "display_categories.html", {'data': data})


# To save inputted data to DB
def save_categories(request):
    if request.method == "POST":
        cn = request.POST.get('cat_name')
        cd = request.POST.get('cat_description')
        c_img = request.FILES['cat_image']
        obj = Category(category_name=cn, category_description=cd, category_image=c_img)
        obj.save()
        return redirect(add_categories_page)


# To edit categories data
def edit_category_page(request, cat_id):
    data = Category.objects.get(id=cat_id)
    return render(request, "edit_categories.html", {'data': data})


# Create function to update edited data
def update_category_page(request, cat_id):
    if request.method == "POST":
        cn = request.POST.get('edit_cat_name')
        cd = request.POST.get('edit_cat_description')
        # Give an exception block to avoid errors while getting image
        try:
            img = request.FILES['edit_cat_image']
            # FileSystem storage need to import
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = Category.objects.get(id=cat_id).category_image
        Category.objects.filter(id=cat_id).update(category_name=cn, category_description=cd, category_image=file)
        return redirect(display_categories)


# create function to delete each data
def delete_category_item(request, cat_id):
    delete_item = Category.objects.filter(id=cat_id)
    delete_item.delete()
    return redirect(display_categories)


# Add products by selecting Category
def add_product_page(request):
    cat = Category.objects.all()
    return render(request, "add-product.html", {'cat': cat})


# To save Products
def save_products(request):
    if request.method == "POST":
        pct = request.POST.get('category_select')
        pn = request.POST.get('product_name')
        pp = request.POST.get('product_price')
        pd = request.POST.get('product_description')
        pimg = request.FILES['product_image']
        obj = Product(pd_category=pct, product_name=pn, product_price=pp, product_description=pd, product_image=pimg)
        obj.save()
    return redirect(add_product_page)


# Create function to display products page
def display_products_page(request):
    pdata = Product.objects.all()
    return render(request, "display_products.html", {'pdata': pdata})


# Create page to edit products
def edit_products_page(request, pro_id):
    cat = Category.objects.all()
    pdata = Product.objects.get(id=pro_id)
    return render(request, "edit_products.html", {'pdata': pdata, 'cat': cat})


# create function to update product edit page
def update_edit_products(request, pro_id):
    if request.method == "POST":
        ecs = request.POST.get('edit_category_select')
        epn = request.POST.get('edit_product_name')
        epp = request.POST.get('edit_product_price')
        epd = request.POST.get('edit_product_description')
        try:
            ep_img = request.FILES['edit_product_image']
            fs = FileSystemStorage()
            file = fs.save(ep_img.name, ep_img)
        except MultiValueDictKeyError:
            file = Product.objects.get(id=pro_id).product_image
        Product.objects.filter(id=pro_id).update(pd_category=ecs, product_name=epn, product_price=epp,
                                                 product_description=epd, product_image=file)
    return redirect(display_products_page)


# create function to delete product item

def delete_product_item(request, pro_id):
    del_pro = Product.objects.get(id=pro_id)
    del_pro.delete()
    return redirect(display_products_page)


def login_page(request):
    return render(request, "admin_login.html")


def admin_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')
        if User.objects.filter(username__contains=un).exists():
            x = authenticate(username=un, password=pwd)
            if x is not None:
                login(request, x)
                request.session['username'] = un
                request.session['password'] = pwd
                return redirect(index_page)
            else:
                return redirect(login)
        else:
            return redirect(login)


def feedback_page(request):
    f_data = Contact.objects.all()
    return render(request, "feedBack.html", {'f_data': f_data})


def feedback_data_delete(request, f_id):
    x = Contact.objects.get(id=f_id)
    x.delete()
    return redirect(feedback_page)