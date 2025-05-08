from django.shortcuts import render, get_object_or_404
from .models import FoodListing, FoodRequest
from django.shortcuts import render, redirect
from .forms import FoodListingForm
from .models import FoodListing
from django.conf import settings

def food_listings(request):
    listings = FoodListing.objects.filter(is_available=True)
    listings = FoodListing.objects.filter(is_available=True).select_related('donor')
    return render(request, 'donation/food_listing.html', {
        'listings': listings,
        'MEDIA_URL': settings.MEDIA_URL  # Pass this to template
    })
 

def food_detail(request, listing_id):
    listing = get_object_or_404(FoodListing, id=listing_id)
    return render(request, 'donation/food_detail.html', {'listing': listing})

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, NGORegistrationForm
from .models import User, NGOProfile
def ngo_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_ngo:
            login(request, user)
            return redirect('ngo_dashboard')
    return render(request, 'donation/login.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_ngo = False
            user.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'donation/register_user.html', {'form': form})

def register_ngo(request):
    if request.method == 'POST':
        form = NGORegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                is_ngo=True
            )
            
            # Create NGO profile
            ngo_profile = form.save(commit=False)
            ngo_profile.user = user
            ngo_profile.save()
            
            login(request, user)
            return redirect('ngo_dashboard')
    else:
        form = NGORegistrationForm()
    
    return render(request, 'donation/register_ngo.html', {'form': form})

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from .forms import FoodListingForm

@login_required
def user_dashboard(request):
    if request.method == 'POST':
        form = FoodListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.save()
            return redirect('user_dashboard')
    else:
        form = FoodListingForm()
    
    listings = FoodListing.objects.filter(donor=request.user)
    return render(request, 'donation/user_dashboard.html', {
        'form': form,
        'listings': listings
    })

@login_required
def ngo_dashboard(request):
    available_listings = FoodListing.objects.filter(is_available=True)
    return render(request, 'donation/ngo_dashboard.html', {
        'listings': available_listings
    })




def create_listing(request):
    if request.method == "POST":
        form = FoodListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)  # Don't save to DB yet
            listing.donor = request.user  # Assign the logged-in user as donor
            listing.save()  # Now save to DB

            # Redirect to respective dashboard
            if request.user.is_ngo:
                return redirect('ngo_dashboard')
            else:
                return redirect('user_dashboard')
    else:
        form = FoodListingForm()
    
    return render(request, 'donation/create_listing.html', {'form': form})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodListing, FoodRequest
from .forms import FoodRequestForm

@login_required
def request_food(request, listing_id):
    food_listing = get_object_or_404(FoodListing, id=listing_id)
    
    if request.method == 'POST':
        form = FoodRequestForm(request.POST)
        if form.is_valid():
            food_request = form.save(commit=False)
            food_request.food_listing = food_listing
            food_request.requester = request.user
            food_request.save()
            return redirect('food_detail', listing_id=listing_id)
    else:
        form = FoodRequestForm()
    
    return render(request, 'donation/request_food.html', {
        'form': form,
        'food_listing': food_listing
    })

@login_required
def manage_request(request, request_id, action):
    food_request = get_object_or_404(FoodRequest, id=request_id)
    
    # Verify the current user is the donor
    if request.user != food_request.food_listing.donor:
        return redirect('food_listing')
    
    if action == 'approve':
        food_request.status = 'approved'
        food_request.food_listing.is_available = False
        food_request.food_listing.save()
    elif action == 'reject':
        food_request.status = 'rejected'
    
    food_request.save()
    return redirect('user_dashboard')