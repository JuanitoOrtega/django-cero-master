from django.shortcuts import render
from core.erp.models import Category


# Create your views here.
def home(request):
    return render(request, 'home.html')