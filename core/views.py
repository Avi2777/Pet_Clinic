from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from users.forms import CustomUserCreationForm

# Create your views here.

User = get_user_model()


# --- Login and Logout Views ---
login_view = LoginView.as_view(template_name='core/login.html')
logout_view = LogoutView.as_view()


# --- Custom Signup View ---
class CustomSignupView(FormView):
    template_name = 'core/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('core:dashboard')  # Redirect to the dashboard after successful signup

    def form_valid(self, form):
        # Create a new user using the form data and save it
        user = form.save()
        # Redirect to the dashboard
        return redirect(self.success_url)

    def form_invalid(self, form):
        # Handle the case when the form data is invalid

        return super().form_invalid(form)


# --- Landing Page View ---
def landing_view(request):
    users = User.objects.all()
    return render(request, 'core/landing_page.html', {'users': users})


# --- Dashboard View ---
@login_required
def dashboard_view(request):

        if request.method == 'POST':
            # Your logic for staff users to handle the form submission (if needed)
            return redirect('core:dashboard')  # Redirect after successful form submission
        else:
            # Display the admin dashboard page without any form submissions
            users = User.objects.all()
            # Your other staff-related logic (if needed)
            return render(request, 'core/dashboard.html', {'users': users})


# --- User Profile View ---
@login_required
def user_profile_view(request):
    user = request.user
    return render(request, 'core/my_profile.html', {'user': user})