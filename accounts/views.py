from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customers')
            user.group.add(group)
            Customers.objects.create(user=user)
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username and Password is incorrect')

    return render(request, 'accounts/login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customers.objects.all()

    totalCustomers = customers.count()

    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'customers': customers,
        'orders': orders,
        'totalOrders': totalOrders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customers.order_set.all()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 
               'totalOrders': totalOrders,
               'delivered': delivered,
               'pending': pending, }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
    customer= request.user.customers
    form= CustomerForm(instance=customer)
    if request.method== 'POST':
        form=CustomerForm(request.POST,request.FILES,instance= customer)
        if form.is_valid():
            form.save()
        

    context={'form': form}

    return render(request, 'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_test):
    customer = Customers.objects.get(id=pk_test)
    orders = customer.order_set.all()
    ordersCount = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'ordersCount': ordersCount,
    }

    return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def village(request):
    return render(request, 'folder/village.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk_test):
    customer = Customers.objects.get(id=pk_test)
    form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk_test):
    order = Order.objects.get(id=pk_test)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk_test):
    order = Order.objects.get(id=pk_test)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {
        'item': order
    }

    return render(request, 'accounts/delete.html', context)
