from django.shortcuts import render


# Create your views here.


def roomStaffHomePage(request):
    return render(request, 'roomStaffHomePage.html')
