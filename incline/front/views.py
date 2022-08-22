from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages #login was successful! etc

def home(request):
    return render(request, 'front/home.html', {})

def docs(request):
    views = open("user/views.py", "r")
    urls = open("user/urls.py", "r")
    models = open("user/models.py", "r")
    manage = open("manage.py", "r")

    base = open("user/templates/user/base.html", "r")
    contracts = open("user/templates/user/contracts.html", "r")
    help = open("user/templates/user/help.html", "r")
    login = open("user/templates/user/login.html", "r")
    new_contract = open("user/templates/user/new_contract.html", "r")
    register = open("user/templates/user/register.html", "r")
    home = open("front/templates/front/home.html", "r")
    
    return render(request, 'front/docs.html', {"views": views.read(), "urls": urls.read(), "models": models.read(), "base": base.read(), "contracts": contracts.read(), "help": help.read(), "login": login.read(), "new_contract": new_contract.read(), "register": register.read(), "home": home.read()})

def about(request):
    return render(request, 'front/about.html', {})

def media(request, filename):
    return render(request, 'front/media.html', {'Filename': filename})

def help(request):
    return render(request, 'front/help.html', {})
