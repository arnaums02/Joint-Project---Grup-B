from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm
from accounts.forms import SignInForm
from accounts.models import CustomUser


# Create your views here.

def signIn(request):
    if request.method == 'POST':

        email = request.POST['email']

        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('homePage')

        else:
            messages.error(request,'Correo electrónico o contraseña incorrectos.')
            return render(request, 'signIn.html')

    return render(request, 'signIn.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homePage')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})
