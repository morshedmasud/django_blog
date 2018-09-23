from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "index.html")

def getauthor(request, name):
    return render(request, "profile.html")

def getsingle(request, id):
    return render(request, "single.html")