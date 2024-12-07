from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdatedForm, ProfileUpdateForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
    # Check if update mode is enabled from the query parameters
    is_update_mode = request.GET.get('mode') == 'update'

    if request.method == 'POST' and is_update_mode:
        # Handle form submission when in update mode
        u_form = UserUpdatedForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated successfully!')
            return redirect('profile')  # Redirect to the profile page after successful update
    
    elif request.method == 'POST' and 'delete_account' in request.POST:
        # If 'delete_account' POST is sent, display confirmation page
        user = request.user
        
        # If confirmation is made, delete the account
        if 'confirm' in request.POST:
            # Delete the user's profile image if it exists
            if user.profile.image:
                user.profile.image.delete()

            # Delete the user's profile and user account
            user.profile.delete()
            user.delete()

            messages.success(request, f'Your account has been deleted successfully.')
            logout(request)  # Log out the user after account deletion
            return redirect('register')  # Redirect to the registration page after deletion
        
        # If no confirmation, render the confirmation page
        return render(request, 'users/delete_account_confirmation.html', {'user': user})

    else:
        # Initialize the forms, with existing data
        u_form = UserUpdatedForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'is_update_mode': is_update_mode,  # Pass the mode to the template
    }
    return render(request, 'users/profile.html', context)  # Render the profile page
