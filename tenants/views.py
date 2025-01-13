from django.shortcuts import render


def tenant(request):
    return render(request, 'tenants.html')
