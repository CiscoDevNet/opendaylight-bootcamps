from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def emu(request):
    return render(request, 'emu.html')