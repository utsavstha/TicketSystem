from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from core.models import Account
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm


def users(request):
    users = Account.objects.all()
    context = {'activate_users': 'active', 'users': users}
    return render(request, 'users/users.html', context)


def create_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users')

    context = {'activate_users': 'active', 'form': form}
    return render(request, 'users/users_form.html', context)


def update_user(request, pk):
    user = Account.objects.get(id=pk)
    form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # user.set_password(form.cleaned_data.get('password'))
            # user.save()
            return redirect('/users')
    context = {'activate_users': 'active', 'form': form}
    return render(request, 'users/users_form.html', context)


def delete_user(request, pk):
    user = Account.objects.get(id=pk)
    user.delete()

    return redirect('/users')


def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("success")

            return redirect('boards')
        else:
            print("failed")
            print(username)
            messages.add_message(request, messages.ERROR,
                                 'Login Failed')
            return render(request, 'users/login.html')
    return render(request, 'users/login.html')


def register_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and email and password:
            user, created = User.objects.get_or_create(
                username=username, email=email)
            if created:
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('users')
            # user was created
            # set the password here
            else:
                messages.add_message(request, messages.ERROR,
                                     'User already exists')
                return render(request, 'users/register.html')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Registration Failed')
            return render(request, 'users/register.html')
    return render(request, 'users/register.html')


# def change_password(request):
#     if request.method == 'POST':
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         pk = request.POST.get('user')

#         if username and password1 and password2 and password1 == password2:
#             user = Account.objects.get(id=pk)
#             user.password = make_password(password1)
#             user.save()

#             return redirect('boards')

#         else:
#             messages.add_message(request, messages.ERROR,
#                                  'Registration Failed')
#             return render(request, 'users/password.html')
#     return render(request, 'users/password.html')
def change_password(request, pk):
    user = Account.objects.get(id=pk)
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            user.set_password(password2)
            user.save()
            return redirect('/users')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Passwords do not match')
    context = {'activate_users': 'active'}
    return render(request, 'users/password.html', context)


def logout_request(request):
    logout(request)
    return redirect('login')
