from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Ingredient,Garnish
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
from django.shortcuts import render, redirect,resolve_url
from django.urls import reverse
from openai import OpenAI
import json
from django.http import JsonResponse
from dotenv import load_dotenv
from .constants import INGREDIENT_PIN_MAPPING,GARNISH_ANGLE_MAPPING
from .arduino import callArduino



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

    video_capture = cv2.VideoCapture(0,cv2.CAP_AVFOUNDATION) # 0 FOR ARDA, 1 FOR ROHAN, HOWARD
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
    garnishes = Garnish.objects.all()
    context = {'ingredients':ingredients, 'garnishes':garnishes}
    return render(request,'ingrediants.html',context)

def products(request):
    return render(request,'products.html')

def suggestions(request):
    ingredients = Ingredient.objects.all()
    garnishes = Garnish.objects.all()

    ingredient_id_map = {i.name: str(i.id - 1) for i in ingredients} 
    garnish_id_map = {g.name: str(g.id - 1) for g in garnishes}

    return render(request, 'suggest.html', {
        'ingredient_id_map': ingredient_id_map,
        'garnish_id_map': garnish_id_map,
    })

def processRequest(request):
    if request.method == 'POST':
        # Get selected ingredients and garnishes
        selected_ingredients = request.POST.getlist('selected_ingredients')
        selected_garnishes = request.POST.getlist('selected_garnish')

        # Get the actual ingredient and garnish names from the DB
        ingredient_names = list(Ingredient.objects.all().values_list('name', flat=True))
        ingredient_amount = list(Ingredient.objects.all().values_list('amount', flat=True))
        ingredient_amount_string = [str(amount) for amount in ingredient_amount]
        garnish_names = list(Garnish.objects.all().values_list('name', flat=True))
        print(ingredient_names)
        print(ingredient_amount_string)
        print(garnish_names)

        user_prompt = request.POST.get('request', '').strip() 

        # Construct the prompt
        request_prompt = f"""
        You are an assistant to a bartender.

        The user has requested the following: "{user_prompt}"
        Given the following available ingredients: {', '.join(ingredient_names)}.
        Their respective amounts left: {', '.join(ingredient_amount_string)}.
        And the following garnishes: {', '.join(garnish_names)}.
        Come up with a drink recipe using some or all of these ingredients, only use ingredient we have.
        Some ingrediants have run out, so don't come up with a recipe without enough ingredient to make it.
        Unless user specifies, make the portion size for the drink VERY SMALL.


        Respond in the following JSON format only (no extra explanation):

        {{
            "drink_name": "<name of drink>",
            "recipe": [
                {{"ingredient": "<ingredient name>", "amount_ml": <amount in mL>}},
                ...
            ],
            "garnish": "<optional garnish if used>"
        }}
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful bartender assistant. Return only valid JSON responses."},
                    {"role": "user", "content": request_prompt}
                ],
                temperature=0.7,
                max_tokens=300,
            )
            response_data = response.choices[0].message.content.strip()
            
            # Try to parse the response to JSON
            try:
                drink_json = json.loads(response_data)
                print(response_data)
                return JsonResponse(drink_json)
            except json.JSONDecodeError as e:
                print("Failed to decode JSON:", e)
                return JsonResponse({
                    'error': 'Invalid JSON from ChatGPT',
                    'raw_response': response_data
                }, status=500)

        except Exception as e:
            print("OpenAI API error:", e)
            return JsonResponse({'error': 'Failed to contact ChatGPT'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def submitCart(request):
    if request.method == 'POST':
        selected_indices = request.POST.getlist('selected_ingredients')
        selected_garnish_list = request.POST.getlist('selected_garnish')
        selected_garnish_index = selected_garnish_list[0]

        selected_amounts = {}
        
        # For debugging: print the selected indices
        for indice in selected_indices:
            amount_key = f"amount_{indice}_hidden"  # Corresponding hidden input field for the amount
            amount_value = request.POST.get(amount_key)
            if amount_value:
                selected_amounts[indice] = float(amount_value)
            else:
                print(f"amount for indice: {indice} not found")

            
        
        sendArduino(selected_indices,selected_amounts,selected_garnish_index)
        for index in selected_indices:
            db_index = int(index) + 1
            ingredient = Ingredient.objects.get(id = db_index)
            if ingredient:
                amount_used = selected_amounts[index]
                if ingredient.amount >= amount_used:
                    ingredient.amount -= amount_used
                    ingredient.save()
                    print(f"Updated {ingredient.name} amount to {ingredient.amount} mL")
                else:
                    print(f"Error: Not enough amount for {ingredient.name}")
    
    return redirect('ingredients')

def sendArduino(selected_indices,selected_amounts,selected_garnish_index):
    
    print("Ready to send")
    pins_dict = {}
    for index in selected_indices:

        corresponding_amount = selected_amounts[index]
        corresponding_pin = INGREDIENT_PIN_MAPPING[index]
        pins_dict[corresponding_pin] = corresponding_amount
    
        garnishAngle = GARNISH_ANGLE_MAPPING[selected_garnish_index]


    
    print(pins_dict)
    print(garnishAngle)
    callArduino(pins_dict,garnishAngle)


    
    return



   















