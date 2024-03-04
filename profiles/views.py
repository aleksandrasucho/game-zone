from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Address
from .forms import ProfileForm, AddressForm

class ProfileView(LoginRequiredMixin, View):
    """View for displaying user profile."""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = request.user.profile
            addresses = profile.addresses.all()
            return render(request, 'profile.html', {'profile': profile, 'addresses': addresses})
        else:
            return render(request, 'account/login.html')

class EditUserProfileView(LoginRequiredMixin, View):
    """View for editing user profile."""

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'profiles/edit_profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'profiles/edit_profile.html', {'form': form})

class ResetAvatarView(LoginRequiredMixin, View):
    """View for resetting user avatar."""

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        if profile.avatar:
            profile.avatar.delete()  # Delete the avatar file
            profile.avatar = None
            profile.save()
        return redirect('profile')

class EditAvatarAjaxView(LoginRequiredMixin, View):
    """View for editing user avatar using AJAX."""

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            profile = request.user.profile
            new_avatar = request.FILES.get('avatar')
            if new_avatar != profile.avatar:
                profile.avatar = new_avatar
                profile.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)

class AddressesView(LoginRequiredMixin, View):
    """View for displaying user addresses."""

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        addresses = profile.addresses.all()
        return render(request, 'profiles/addresses.html', {'profile': profile, 'addresses': addresses})

class AddAddressView(LoginRequiredMixin, View):
    """View for adding a new address."""

    def get(self, request, *args, **kwargs):
        form = AddressForm()
        return render(request, 'profiles/add_address.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.profile = request.user.profile
            address.save()
            return redirect('addresses')
        return render(request, 'profiles/add_address.html', {'form': form})

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

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return redirect('logout')

    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/delete_profile.html')