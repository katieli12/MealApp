from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature
from urllib.request import urlopen
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        meal = urllib.request.urlopen('https://www.themealdb.com/api/json/v1/1/random.php').read()
        json_data = json.loads(meal)

        ingredientList = ""
        measure = "strMeasure"
        ingred = "strIngredient"
        num = ""
        count = 1
        while (count<21):
            num = measure + str(count)
            ingredientList = ingredientList + str(json_data['meals'][0][num]) + " "
            num = ingred + str(count)
            ingredientList = ingredientList + str(json_data['meals'][0][num]) + "     "
            count = count + 1
            
        data = {
            "mealName": str(json_data['meals'][0]['strMeal']),
            "mealCategory": "Category: " + str(json_data['meals'][0]['strCategory']),
            "mealArea": "Region: " + str(json_data['meals'][0]['strArea']),
            "mealIngredients": ingredientList,
            "mealInstructions": str(json_data['meals'][0]['strInstructions']),
            "mealImage": str(json_data['meals'][0]['strMealThumb']),
        }
    else:
        data = {}
    return render(request, 'index.html', data)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Password Does Not Match')
            return redirect('register')
    else:
        return render(request, 'register.html')
    
def saved(request):
    return render(request, 'saved.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
        
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def counter(request): 
    posts = [1, 2, 3, 4, 5, 'tim', 'tom', 'john']
    return render(request, 'counter.html', {'posts': posts})

def post(request, pk):
    return render(request, 'post.html', {'pk': pk})