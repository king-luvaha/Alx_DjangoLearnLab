from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from django.contrib import messages

# Registration view
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Profile view
@login_required
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get('email')
        request.user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    return render(request, 'registration/profile.html')

# Login view (built-in)
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Logout view (built-in)
class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
