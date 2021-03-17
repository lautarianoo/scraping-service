import ast
import sys

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from django.contrib import messages
import datetime as dt

from scraping.models import Errors
from users.forms import UserLoginForm, UserRegisterForm, UserUpdateForm, ContactForm

User = get_user_model()

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def register_view(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(request, 'users/register_done.html', {'new_user': new_user})
    return render(request, 'users/register.html', {'form': form})

def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.name = data['name']
                user.city = data['city']
                user.prof = data['prof']
                user.send_email = data['send_email']
                user.save()
                return redirect('users:update')
        form = UserUpdateForm(initial={'city': user.city, 'prof': user.prof, 'send_email': user.send_email, 'name': user.name})
        return render(request, 'users/update.html', {'form': form, 'contact_form': contact_form})
    else:
        return redirect('users:login')

def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
    return redirect('index')

#не используется(мб починю)
#def contact_view(request):
    #if request.method == 'POST':
        #contact_form = ContactForm(request.POST or None)
        #if contact_form.is_valid():
            #data = contact_form.cleaned_data
            #city = data.get('city')
            #prof = data.get('prof')
            #email = data.get('email')
            #qs = Errors.objects.filter(timestamp=dt.date.today())
            #if qs.exists():
                #err = qs.first()
                #err.data = ast.literal_eval(err.data)
                #data = err.data.get('user_data', [])
                #data.append({'city': city, 'email': email, 'prof': prof})
                #err.data['user_data'] = data
                #err.save()
            #else:
                #data = {'city': city, 'email': email, 'prof': prof}
                #Errors(data=f"{data}").save()
            #return redirect('users:update')
        #else:
            #redirect('users:update')
    #else:
        #redirect('users:login')