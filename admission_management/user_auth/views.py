from django.shortcuts import render

def authIndex(request):
    return render(request, "auth_login.html")

