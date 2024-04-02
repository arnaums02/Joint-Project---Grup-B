from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.forms import SignInForm


# Create your views here.

def signIn(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)

        password = request.POST['password']
        print(password)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('roomStaffHomePage')

        else:
            messages.error(request,'Correo electrónico o contraseña incorrectos.')
            return render(request, 'signIn.html')

    return render(request, 'signIn.html')

