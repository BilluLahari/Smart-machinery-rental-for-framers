from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Equipment, RentalRequest
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "base.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect("renter_dashboard")
            else:
                return redirect("farmer_dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_staff = request.POST.get("is_staff")  # Convert "on" to True

        try:
            if User.objects.filter(username=username).exists():
                raise ValidationError("Username already exists.")

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_staff
            )
            return redirect("login")
        except ValidationError as e:
            return render(request, "register.html", {"errors": e.messages})
    return render(request, "register.html")


@login_required
def farmer_dashboard(request):
    return render(request, "farmer_dashboard.html")


@login_required
def renter_dashboard(request):
    rental_requests = RentalRequest.objects.filter(renter=request.user)
    return render(request, "renter_dashboard.html", {"rental_requests": rental_requests})


@login_required
def available_equipment(request):
    equipment = Equipment.objects.all()
    return render(request, "available_equipment.html", {"equipment_list": equipment})


@login_required
def renter_equipument(request):
    equipument = Equipment.objects.filter(renter_name = request.user)
    return render(request, "available_equipment_renter.html", {"equipment_list": equipument})

@login_required
def add_machinery(request):
    try:
        if request.method == 'POST':
            # Get the data from the form
            name = request.POST.get('name')
            description = request.POST.get('description')
            price_per_day = request.POST.get('price_per_day')
            price_per_hour = request.POST.get('price_per_hour')
            price_per_week = request.POST.get('price_per_week')
            price_per_15_days = request.POST.get('price_per_15_days')
            price_per_month = request.POST.get('price_per_month')
            image = request.FILES.get('image')  # Get the image file
            
            # Create a new Equipment object and save it to the database
            equipment = Equipment(name=name, description=description, price_per_day=price_per_day,price_per_hour= price_per_hour,price_per_week=price_per_week,price_per_15_days=price_per_15_days,price_per_month=price_per_month, image=image,renter_name=request.user)
            equipment.save()

            return redirect('equipment_list')  # Redirect to the equipment list page (or wherever you want)

        return render(request, 'add_equipment.html')
    except Exception as E:
        return render(request, 'add_equipment.html',{"Exception":E})


@login_required
def request_rental(request, machinery_id):
    machinery = Equipment.objects.get(id=machinery_id)
    RentalRequest.objects.create(machinery=machinery, renter=request.user)
    machinery.available = False
    machinery.save()
    return redirect("farmer_dashboard")


@login_required
def approve_request(request, request_id):
    rental_request = RentalRequest.objects.get(id=request_id)
    rental_request.approved = True
    rental_request.save()
    return redirect("renter_dashboard")


def user_logout(request):
    logout(request)
    return redirect("login")

def admin_dashboard(request):
    # Get all rental requests from the database
    rental_requests = RentalRequest.objects.all()

    # Render the admin dashboard template with rental requests data
    return render(request, 'admin_dashboard.html', {'rental_requests': rental_requests})


def my_rentals(request):
    # Get rental requests made by the logged-in user
    rental_requests = RentalRequest.objects.filter(renter=request.user)
    
    return render(request, 'my_rentals.html', {
        'rental_requests': rental_requests
    })

@login_required
def view_requests(request):
    # Only admin users can access this view
    if not request.user.is_staff:
        return redirect('home')  # Redirect to home if the user is not admin
    
    # Fetch all rental requests
    rental_requests = RentalRequest.objects.all()
    
    return render(request, 'view_requests.html', {
        'rental_requests': rental_requests
    })

@login_required
def reject_request(request, request_id):
    # Only admin users can reject
    if not request.user.is_staff:
        return redirect('home')  # Redirect if not an admin
    
    rental_request = get_object_or_404(RentalRequest, id=request_id)
    rental_request.status = 'Rejected'
    rental_request.save()
    
    return redirect('view_requests') 

def equipment_list(request):
    # Fetch all available equipment
    equipment_list = Equipment.objects.filter(renter_name=request.user)
    return render(request, 'equipment_list.html', {'equipment_list': equipment_list})


@login_required
def update_machinery(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Get the image file
        
        # Create a new Equipment object and save it to the database
        equipment = Equipment(name=name, description=description, price_per_day=price, image=image)
        equipment.save()

        return redirect('equipment_list')  # Redirect to the equipment list page (or wherever you want)

    return render(request, 'add_equipment.html')

def update_equipment(equipment, name, description, price_per_day,price_per_15_days,price_per_week,price_per_month, image):
    # Function to update existing equipment
    equipment.name = name
    equipment.description = description
    equipment.price_per_day = price_per_day
    if image:  # Update the image only if a new one is provided
        equipment.image = image
    equipment.save()  # Save the updated equipment

@login_required
def update_machinery(request, equipment_id):
    try:
        equipment = Equipment.objects.get(id=equipment_id)
    except Equipment.DoesNotExist:
        return redirect('equipment_list')  # Redirect if equipment does not exist

    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        description = request.POST.get('description')
        price_per_day = request.POST.get('price_per_day')
        price_per_15_days = request.POST.get('price_per_15_days')
        price_per_week = request.POST.get('price_per_week')
        price_per_month = request.POST.get('price_per_month')
        image = request.FILES.get('image')  # Get the image file

        # Call the update_equipment function to update the existing equipment
        update_equipment(equipment, name, description, price_per_day,price_per_15_days,price_per_week,price_per_month, image)

        return redirect('equipment_list')  # Redirect to the equipment list page (or wherever you want)

    # Pre-populate the form with the existing equipment details
    return render(request, 'update_equipment.html', {'equipment': equipment})


@login_required
def delete_machinery(request,equipment_id):
    try:
        equipument = Equipment.objects.get(id=equipment_id)
    except Equipment.DoesNotExist:
        return redirect('equipment_list')
    
    equipument.delete()
    
    return redirect('renter_dashboard')
