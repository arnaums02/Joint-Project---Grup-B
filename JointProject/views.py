from django.shortcuts import render, redirect

from .forms import SignInForm
from .models import UserRoomStaff


# Create your views here.
def signIn(request):
    form = SignInForm(request.POST)
    context = {
        'form': form
    }
    if context['form'].is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        if authentificateRoomStaffUser(email, password):
            return redirect('roomStaffHomePage')
        else:
            form.add_error(None, 'Correo electrónico o contraseña incorrectos.')
    return render(request, 'signIn.html', context)


def authentificateRoomStaffUser(email, password):
    try:
        user = UserRoomStaff.objects.get(email=email)
        if password == user.password:
            return True
        else:
            return False
    except UserRoomStaff.DoesNotExist:
        return False


def roomStaffHomePage(request):
    return render(request, 'roomStaffHomePage.html')
