from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Equipment, RentalRequest
from django.contrib.auth.decorators import user_passes_test

# Add new equipment
@login_required
def add_equipment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price_per_day = request.POST.get("price_per_day")
        price_per_week = request.POST.get("price_per_week")
        price_per_15days = request.POST.get("price_per_15days")
        price_per_month = request.POST.get("price_per_month")
        equipment = Equipment(
            name=name,
            description=description,
            price_per_day=price_per_day,
            price_per_week=price_per_week,
            price_per_15days=price_per_15days,
            price_per_month=price_per_month,
        )
        equipment.save()
        return redirect('admin_dashboard')
    return render(request, 'admin/add_equipment.html')

# Approve or reject requests
@login_required
def view_requests(request):
    requests = RentalRequest.objects.all()
    return render(request, 'admin/view_requests.html', {'requests': requests})

@login_required
def change_request_status(request, request_id, status):
    rental_request = get_object_or_404(RentalRequest, id=request_id)
    rental_request.status = status
    rental_request.save()
    return redirect('view_requests')


# Check if the user is an admin
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admins').exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Admin-specific functionality
    return render(request, 'admin/admin_dashboard.html')
