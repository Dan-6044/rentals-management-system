from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.urls import reverse
from .models import Property, PropertyImage, PropertyVideo
from django.http import JsonResponse
from django.http import HttpResponseForbidden



User = get_user_model()

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the home page


def landlord(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Create the new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_id = user.id  # Get the user's ID

            # Log the user in automatically after registration
            login(request, user)

            return redirect('dashboard', user_id=user_id)  # Redirect to home after successful registration
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user exists with the provided email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            # Authenticate using the username (not email)
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                # Log the user in
                auth_login(request, authenticated_user)
                return redirect(reverse('dashboard', args=[authenticated_user.id]))
            else:
                # Password mismatch
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            # Email not found
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'login.html')


def contact(request):
    return render(request, 'contact-page.html')


@login_required
def dashboard(request, user_id):
    # Ensure the logged-in user matches the user_id
    if request.user.id != user_id:
        return redirect('dashboard', user_id=request.user.id)
    
    # Retrieve the properties associated with the user
    user = get_object_or_404(User, id=user_id)
    properties = Property.objects.filter(user=user)
    
    # Render the dashboard template with the user and their properties
    return render(request, 'dashboard.html', {'user': user, 'properties': properties})


@login_required
def add_property(request, user_id):
    # Ensure the logged-in user matches the user_id in the URL
    if request.user.id != user_id:
        messages.error(request, "You cannot add properties for other users.")
        return redirect('dashboard', user_id=request.user.id)  # Redirect to the logged-in user's dashboard

    if request.method == "POST":
        # Fetch property details from the POST request
        property_name = request.POST.get('property_name')
        property_type = request.POST.get('property_type')
        layout = request.POST.get('layout')
        location = request.POST.get('location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        features = request.POST.get('features')
        rent = request.POST.get('rent')
        agency = request.POST.get('agency', '')  # Optional field
        amenities = request.POST.get('amenities')
        terms = request.POST.get('terms')
        contact = request.POST.get('contact')
        
        # Handle the main image (first image)
        image = request.FILES.get('image')

        # Ensure all required fields are provided
        if not all([property_name, property_type, layout, location, features, rent, amenities, terms, contact, image]):
            messages.error(request, "All fields must be filled out.")
            return redirect('add-property', user_id=user_id)

        # Create and save the property
        property = Property(
            user=request.user,  # Link the property to the logged-in user
            property_name=property_name,
            property_type=property_type,
            layout=layout,
            location=location,
            latitude=latitude,
            longitude=longitude,
            features=features,
            rent=rent,
            agency=agency,
            amenities=amenities,
            terms=terms,
            contact=contact,
            image=image  # Save the main image
        )
        property.save()

        # Handle multiple images (save all images selected in the form)
        if 'images' in request.FILES:
            for img in request.FILES.getlist('images'):
                PropertyImage.objects.create(property=property, image=img)

        # Handle multiple videos (save all videos selected in the form)
        if 'videos' in request.FILES:
            for video in request.FILES.getlist('videos'):
                PropertyVideo.objects.create(property=property, video=video)

        messages.success(request, "Property added successfully!")
        return redirect('dashboard', user_id=user_id)  # Redirect back to the logged-in user's dashboard

    return render(request, 'add_property.html')


@login_required
def property_detail(request, property_id):
    # Fetch the specific property by ID
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'property_detail.html', {'property': property, 'user': request.user})


@login_required
def update_property(request, property_id):
    try:
        # Fetch the property by ID and ensure it belongs to the logged-in user
        property = Property.objects.get(id=property_id, user=request.user)

        if request.method == 'POST':
            # Update property details
            property.property_name = request.POST.get('property_name', property.property_name)
            property.property_type = request.POST.get('property_type', property.property_type)
            property.layout = request.POST.get('layout', property.layout)
            property.location = request.POST.get('location', property.location)
            property.features = request.POST.get('features', property.features)
            property.amenities = request.POST.get('amenities', property.amenities)
            property.terms = request.POST.get('terms', property.terms)
            property.rent = request.POST.get('rent', property.rent)
            property.contact = request.POST.get('contact', property.contact)
            property.agency = request.POST.get('agency', property.agency)

            # Check if an image is provided
            if 'image' in request.FILES:
                property.image = request.FILES['image']

            # Save changes
            property.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
    except Property.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Property not found.'}, status=404)


def delete_property(request, property_id):
    if request.method == 'POST':  # Ensure only POST requests are allowed
        property_to_delete = get_object_or_404(Property, id=property_id)
        
        # Optional: Check if the user has permission to delete
        # if request.user != property_to_delete.owner:  # Replace 'owner' with the actual field if needed
        #     return HttpResponseForbidden("You don't have permission to delete this property.")

        property_to_delete.delete()
        messages.success(request, "Property deleted successfully.")
        
        # Redirect to the dashboard or properties list (ensure 'dashboard' is a valid URL name)
        return redirect('dashboard', user_id=request.user.id)  # Use request.user.id instead of user_id

    return HttpResponseForbidden("Invalid request method.")


