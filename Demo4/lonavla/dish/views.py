from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def dish(request):
    if request.method == 'POST':
        
        @login_required(login_url='/login/')  
        def add_dish(request):                             # Define the function for adding a dish
            data = request.POST
            dish_name = data.get('dish_name')
            dish_description = data.get('dish_description')
            dish_image = request.FILES.get('dish_image')

            Dish.objects.create(
                dish_name=dish_name,
                dish_description=dish_description,
                dish_image=dish_image,
            )
            return redirect('/dish/')
        return add_dish(request)                        # Call the function to add a dish
    
    if not request.user.is_authenticated:                # Display a message for unauthenticated users
        messages.info(request, 'Please log in to add a dish.')

    queryset = Dish.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(dish_name__icontains = request.GET.get('search'))
    context = {'dish': queryset}
    return render(request, 'dish.html', context)

@login_required(login_url='/login/')
def delete(request,id):
    #print(id)
    queryset = Dish.objects.get(id=id)
    queryset.delete()
    return redirect('/dish/')

@login_required(login_url='/login/')
def update(request,id):
    queryset = Dish.objects.get(id=id)

    if request.method == 'POST':
        data = request.POST
        dish_name = data.get('dish_name')
        dish_description = data.get('dish_description')
        dish_image = request.FILES.get('receipe_image')

        queryset.dish_name = dish_name
        queryset.dish_description = dish_description
        if dish_image:
            queryset.dish_image = dish_image
        queryset.save()
        return redirect('/dish/')
    
    context = {'dish':queryset}
    return render(request,'update.html',context)

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists(): #check if username is correct 
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/dish/')
    return render(request,'login.html')

def log_out(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username :
            messages.error(request,'Username is required')
            return redirect('/register/')
        
        user = User.objects.filter(username = username) #check if somebody else is having same username
        if user.exists():
            messages.error(request,'Username already exists')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
        messages.info(request,'Account created succesfully')
        return redirect('/login/')
    return render(request,'register.html')