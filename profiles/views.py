from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Address
from .forms import ProfileForm, AddressForm
from django.contrib import messages

class ProfileView(LoginRequiredMixin, View):
    """View for displaying user profile."""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = request.user.profile
            addresses = profile.addresses.all()
            return render(request, 'profiles/profile.html', {'profile': profile, 'addresses': addresses})
        else:
            return render(request, 'account/login.html')

class EditUserProfileView(LoginRequiredMixin, View):
    """View for editing user profile."""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=request.user)
            profile_form = ProfileForm(instance=profile)
            address_form = AddressForm(instance=profile.addresses.first())
            return render(request, 'profiles/edit_profile.html', {'profile_form': profile_form, 'address_form': address_form})
        else:
            return render(request, 'account/login.html')

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        address_instance = profile.addresses.first() if profile.addresses.exists() else None
        address_form = AddressForm(request.POST, instance=address_instance)
        if profile_form.is_valid() and address_form.is_valid():
            profile_instance = profile_form.save()
            address_instance = address_form.save(commit=False)
            address_instance.profile = profile_instance
            address_instance.save()
            messages.success(request, 'Changes have been saved.')  # Display success message
            return redirect('profiles:edit_profile')  # Stay on the edit_profile page
        return render(request, 'profiles/edit_profile.html', {'profile_form': profile_form, 'address_form': address_form})

class AddressesView(LoginRequiredMixin, View):
    """View for displaying user addresses."""

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        addresses = profile.addresses.all()
        return render(request, 'profiles/addresses.html', {'profile': profile, 'addresses': addresses})


class EditAddressView(LoginRequiredMixin, View):
    """View for editing an existing address."""

    def get(self, request, address_id, *args, **kwargs):
        address = get_object_or_404(Address, pk=address_id, profile=request.user.profile)
        form = AddressForm(instance=address)
        return render(request, 'profiles/edit_address.html', {'form': form})

    def post(self, request, address_id, *args, **kwargs):
        address = get_object_or_404(Address, pk=address_id, profile=request.user.profile)
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('addresses')
        return render(request, 'profiles/edit_address.html', {'form': form})

class DeleteAddressView(LoginRequiredMixin, View):
    """View for deleting an existing address."""

    def post(self, request, address_id, *args, **kwargs):
        address = get_object_or_404(Address, pk=address_id, profile=request.user.profile)
        address.delete()
        return redirect('addresses')

    def get(self, request, address_id, *args, **kwargs):
        address = get_object_or_404(Address, pk=address_id, profile=request.user.profile)
        return render(request, 'profiles/delete_address.html', {'address': address})

class ChangePrimaryAddressView(LoginRequiredMixin, View):
    """View for changing the primary address."""

    def post(self, request, address_id, *args, **kwargs):
        profile = request.user.profile
        address = get_object_or_404(Address, pk=address_id, profile=profile)
        if address != profile.primary_address:  # Only save if primary address changes
            profile.primary_address = address
            profile.save()
        return redirect('addresses')

class DeleteProfileView(LoginRequiredMixin, View):
    """View for deleting user profile."""

    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/delete_profile.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return HttpResponseRedirect(reverse('home'))  # Redirect to home page
