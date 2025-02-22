from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Ingredient
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .forms import NewFaceForm
import base64
import os
import face_recognition
import cv2
import numpy as np
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from openai import OpenAI
import json
from django.http import JsonResponse
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def homeAction(request):
    return render(request,'home.html')


    

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
                format, imgstr = photo_data.split(';base64,')
                imgdata = base64.b64decode(imgstr)
                image_path = os.path.join(settings.BASE_DIR, 'BarBelt', 'static', f'{name}.jpg')
                request.session['name'] = name
                with open(image_path, 'wb') as f:
                    f.write(imgdata)
                return redirect('login_successful') 

    return render(request, 'take_photo.html', {'form': NewFaceForm()})


def facialRecognition(request):

# Load a sample picture and learn how to recognize it.
    image_folder_path = os.path.join(settings.BASE_DIR,'BarBelt', 'static')
    all_files = os.listdir(image_folder_path)
    face_encodings_dict = {}
    for fileName in all_files:
        if fileName.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(image_folder_path, fileName)
            image = face_recognition.load_image_file(image_path)
            if image is None:
                print("error loading in image")
            face_encodings_dict[fileName] = face_recognition.face_encodings(image)[0]
    

    known_face_encodings = []
    known_face_names = []
    for fileName,encoding in face_encodings_dict.items():
        file_name_without_extension = os.path.splitext(fileName)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(file_name_without_extension)

    # Initialize the webcam

    video_capture = cv2.VideoCapture(1,cv2.CAP_AVFOUNDATION)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return
    while True:
        # Grab a single frame from the webcam
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame")
            break
        

        # Resize the frame to speed up processing (optional)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR (OpenCV) to RGB (face_recognition)
        rgb_small_frame = small_frame[:, :, ::-1]
        rgb_small_frame = cv2.cvtColor(rgb_small_frame , cv2.COLOR_BGR2RGB)

        
        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            # Compare the found faces with known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name =  known_face_names[first_match_index]
                request.session['name'] = name
                return redirect('login_successful')

            else:
                return redirect ('takePhoto')


            
            face_names.append(name)

        if len(face_names) == 0:
            continue

       
        if (cv2.waitKey(1) & 0xFF == ord('q')) or name:
            break

    # Release the webcam and close all OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

def ingredients(request):
    ingredients = Ingredient.objects.all()
    context = {'ingredients':ingredients}
    return render(request,'ingrediants.html',context)

def products(request):
    return render(request,'products.html')

def suggestions(request):
    return render(request,'suggest.html')

def processRequest(request):
    if request.method == 'POST':
        request_prompt = request.POST.get('request')
        print(request_prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can also use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request_prompt}
            ],
        temperature=0.7,
        max_tokens=40)
        response_data = response.choices[0].message.content
        response_dict = {'response': response_data}
        try:
            
            return JsonResponse(response_dict)
        except:
            print("error in json")
            return JsonResponse({'error': 'Invalid JSON response', 'message': response_data}, status=500)

    return JsonResponse({'error': 'Invalid JSON response', 'message': response_data}, status=500)

def submitCart(request):
    if request.method == 'POST':
        selected_indices = request.POST.getlist('selected_ingredients')
        
        # For debugging: print the selected indices
        print(f"Selected Ingredient Indices: {selected_indices}")
    return redirect('ingredients')















