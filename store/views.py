from django.shortcuts import render, redirect
from django.template import loader
from django.http import (HttpResponse,
                         HttpResponseForbidden,
                         HttpResponseBadRequest)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required 
from django.views.generic import View

from django.contrib.auth.forms import PasswordChangeForm
from store.models import Product,Order,Employs,Feedback
from .forms import OrderForm, RegisterForm ,AdminForm, ProductForm,LoginForm,FeedbackForm
from . import helper
from django.contrib.auth.hashers import make_password
import csv,io
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def index(request):
    return render(request, 'base.html', context={})



#Admin views starts from here

def AdminLogin(request):
    form=AdminForm(request.POST or None)
    if request.method == "GET":
        context = {
            'error': False,
            'form':form
        }
        return render(request, 'registration/AdminLogin.html', context=context)

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username = username, password=password)

    if user is not None:
        login(request, user)
        return redirect('adminsite')
    else:
        return render(request, 'registration/AdminLogin.html',
                      context={'error': True})

#admin page
@login_required
def adminsite(request):
    all_products = Product.objects.all()
    all_orders = Order.objects.all()
    return render(request, 'CreatedAdminPage.html', {'all_orders' : all_orders,'all_products' : all_products})


#adding a product by admin
@login_required
def addmeal(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('adminsite')

    return render(request, 'addProduct.html', {'form' : form})

#edit product by admin
@login_required
def editmeal(request,id):
    product = Product.objects.get(id=id)
    form = ProductForm(request.POST or None, instance=product) 

    if form.is_valid():
        form.save()
        return redirect('adminsite')

    context={
        'form' : form,
        'product' : product,
    }
    return render(request, 'editProduct.html', context=context)


#delete product by admin
@login_required
def deletemeal(request, id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        product.delete()
        return redirect('adminsite')

    context={
        'product' : product
    }
    return render(request, 'deleteProductConfirm.html', context=context)




@login_required
def viewfeedback(request):
    all_feedbacks = Feedback.objects.all()
    context={
        'all_feedbacks':all_feedbacks,
    }
    return render(request, 'viewfeedback.html',context=context)





@login_required
def reportDownload(request):
    all_orders=Order.objects.all()
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="Orders Made.csv"'

    writer = csv.writer(response, delimiter=',')
    title=['  ','  ','REPORT', 'FOR',' ORDERS',' MADE ']
    writer.writerow(title) # col by col
    writer.writerow(['EMPLOYEE ', 'FOOD PRODUCT ',' QUANTITY ORDERED ', 'ORDER DESCRIPTION','DATE OF LAST CHANGED '])

    for order in all_orders:
        writer.writerow([order.email,order.meal, order.quantity, order.comments, order.last_change])

    return response



@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('adminsite')
    
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'registration/password_change_form.html', {'form':form})









#employees view starts here



def dashboard(request):
    all_products = Product.objects.all()
    all_orders = Order.objects.all()
    currency = helper.get_currency()
    context= {'all_products' : all_products, 'all_orders':all_orders, 'currency': currency,}
    return render(request,'dashboard.html', context=context)


def loginView(request):
    form=LoginForm(request.POST or None)
    if request.method == "GET":
        context = {
            'error': False,
            'form':form
        }
        return render(request, 'registration/login.html', context=context)

    if form.is_valid():  
        email= request.POST['email']
        password = request.POST['password']
    
        emp = authenticate(request, email = email, password=password)
        return redirect('dashboard')
        
    return render(request, 'registration/login.html', context={'error': True})
            



def logoutView(request):
    return redirect('loginView')



def AddOrder(request):
    list = Product.objects.all
    all_orders = Order.objects.all()
    currency = helper.get_currency()

    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')  

    context = {
        'list': list,
        'currency': currency,
        'form': form,
        'all_orders':all_orders
    }
    return render(request, 'order.html', context=context)


def EditOrderPage(request):
    list = Product.objects.all
    all_orders = Order.objects.all()
    currency = helper.get_currency()

    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('dashboard')

    context = {
        'list': list,
        'currency': currency,
        'form': form,
        'all_orders':all_orders
    }
    return render(request, 'editOrderPage.html', context=context)
    

def EditOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(request.POST or None, instance=order) 
    list = Product.objects.all
    all_orders = Order.objects.all()
    currency = helper.get_currency()


    if form.is_valid():
        form.save()
        return redirect('dashboard')

    context={
        'form' : form,
        'order' : order,
        'list': list,
        'currency': currency,
        'all_orders':all_orders,
    }
    return render(request, 'editOrder.html', context=context)

#register view
class UserFormView(View):
    #blueprint for the form
    form_class= RegisterForm
    template_name='registration/register.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})
        
    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            #take info and store in db but check for validity first

            user = form.save(commit=False)
            #clean (normalised) data
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            department = form.cleaned_data['department']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.password = make_password('password')
            #user.set_password(password)
            user.save()
            return redirect('loginView')

        return render(request, self.template_name, {'form':form})


class FeedbackFormView(View):
    form_class= FeedbackForm
    template_name='feedback.html'

    #display blank form
    def get(self, request):
        form = self.form_class(None)
        all_products = Product.objects.all()
        return render(request, self.template_name, {'form':form,'all_products':all_products})
        
    #process form data
    def post(self, request):
        form = self.form_class(request.POST)
        #all_products = Product.objects.all()

        if form.is_valid():

            #take info and store in db but check for validity first

            feedback = form.save(commit=False)
            #clean (normalised) data
            EmployeeFirstname = form.cleaned_data['EmployeeFirstname']
            EmployeeDepartment = form.cleaned_data['EmployeeDepartment']
            Product = form.cleaned_data['Product']
            Content = form.cleaned_data['Content']

            feedback.save()
            return redirect('dashboard')
        all_products = Product.objects.all()
        return render(request, self.template_name, {'form':form,'all_products':all_products})






