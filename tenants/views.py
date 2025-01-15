from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.urls import reverse



User = get_user_model()

def tenant(request):
    return render(request, 'tenants.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('tenant')  # Redirect to the home page


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_id = user.id  # Get the user's ID

            # Log the user in automatically after registration
            login(request, user)
            return redirect('ten_dashboard', user_id=user_id)  # Redirect to home after successful registration
    else:
        form = SignupForm()

    return render(request, 'signing.html', {'form': form})


def signin(request):
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
                return redirect(reverse('ten_dashboard', args=[authenticated_user.id]))
            else:
                # Password mismatch
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            # Email not found
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'signing.html')


@login_required
def ten_dashboard(request, user_id):
    # Ensure the logged-in user matches the user_id
    if request.user.id != user_id:
        return redirect('ten_dashboard', user_id=request.user.id)
    
    # Retrieve the properties associated with the user
    user = get_object_or_404(User, id=user_id)
    
    
    # Render the dashboard template with the user and their properties
    return render(request, 'properties.html', {'user': user })

