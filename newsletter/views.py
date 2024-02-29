from django.shortcuts import render, redirect
from .forms import SubscriberForm
from .models import Subscriber

def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if the email already exists in the database
            if not Subscriber.objects.filter(email=email).exists():
                subscriber = Subscriber(email=email)
                subscriber.save()
            return redirect('success')
    else:
        form = SubscriberForm()
    return render(request, 'subscribe.html', {'form': form})

def success(request):
    return render(request, 'success.html')