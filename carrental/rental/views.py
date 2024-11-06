from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Car
from django.http import HttpResponse
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        login_option = request.POST.get('login_option')
        username = request.POST['username']
        password = request.POST['password']

        if login_option == 'login_as_user':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after user login
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')  # Redirect back to login page with error

        elif login_option == 'signup':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')  # Redirect to home page after signup
            else:
                messages.error(request, 'Signup failed. Please try again.')
                return redirect('login')  # Redirect back to login page with error

        elif login_option == 'login_as_admin':
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin_home')  # Redirect to admin home page
            else:
                messages.error(request, 'Invalid admin credentials.')
                return redirect('login')  # Redirect back to login page with error

    return render(request, 'rental/login.html')


def home_view(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'rental/home.html', {'cars': cars})

@login_required
def admin_home(request):
    cars = Car.objects.all()
    return render(request, 'rental/admin_home.html', {'cars': cars})

@login_required
def add_car_view(request):
    if request.method == 'POST':
        make = request.POST['make']
        model = request.POST['model']
        price_per_day = request.POST['price_per_day']
        image = request.FILES['image']
        car = Car.objects.create(make=make, model=model, price_per_day=price_per_day, image=image)
        car.save()
        return redirect('admin_home')

    return render(request, 'rental/add_car.html')

def rent_car_view(request, car_id):
    car = Car.objects.get(id=car_id)
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        rental = rental.objects.create(user=request.user, car=car)
        rental.save()
        car.is_available = False
        car.save()
        return render(request, 'rental/thank_you.html', {'car': car})

    return render(request, 'rental/rent_car.html', {'car': car})
