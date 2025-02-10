from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .facial import facialRecognition
from .forms import NewFaceForm
import base64
import os



def homeAction(request):
    return render(request,'home.html')

def facialRecog(request):
    return facialRecognition(request)
    

def takePhoto(request):
    return render(request, 'take_photo.html', {'form': NewFaceForm()})

def login_successful(request):
    name = request.session.get('name', 'Guest')  # Retrieve name from session
    return render(request, 'login_successful.html', {'name': name})

def savePhoto(request):
    if request.method == 'POST':
        form = NewFaceForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')  # Assuming your form has a 'name' field
            if not name:
                print("no name provided")
                return render(request, 'take_photo.html', {'form': NewFaceForm()})


            photo_data = request.POST.get('photo')
            if photo_data:
                # Strip off the prefix (e.g., 'data:image/jpeg;base64,')
                format, imgstr = photo_data.split(';base64,')
                imgdata = base64.b64decode(imgstr)
                image_path = os.path.join(settings.BASE_DIR, 'BarBelt', 'static', f'{name}.jpg')
                request.session['name'] = name
                with open(image_path, 'wb') as f:
                    f.write(imgdata)
                print("success")
                return redirect('login_successful') 
                
    return render(request, 'take_photo.html', {'form': NewFaceForm()})







