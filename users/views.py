from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()  # Render the form if it's a GET request
        
    return render(request, 'users/register.html', {'form': form})  # Render the registration form


class CustomLogoutView(LogoutView):
    template_name = 'users/custom_logout.html'  # Optional: custom template for logout
    next_page = reverse_lazy('login')  # Redirect to 'login' page after logout

@login_required
def profile(request):
    return render (request, 'users/profile.html')