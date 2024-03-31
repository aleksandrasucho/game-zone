from django.shortcuts import render, redirect
from .forms import SubscriberForm
from .models import Subscriber

def subscribe(request):
    """View for subscribing to newsletter."""
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            existing_subscriber = Subscriber.objects.filter(email=email).exists()
            if existing_subscriber:
                # If email already exists, include the error message in the form context
                form.add_error('email', 'You have already subscribed using this email.')
                return render(request, 'subscribe.html', {'form': form})  # Return the form with the error message
            else:
                # Save the form if the email is not already subscribed
                form.save()
                return redirect('success')
    else:
        form = SubscriberForm()
    return render(request, 'subscribe.html', {'form': form})

def success(request):
    """View for displaying subscription success page."""
    return render(request, 'success.html')