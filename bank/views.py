from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import RegistrationForm, LoginForm

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            User.objects.create(username=username, password=password)
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                messages.success(request, f"Welcome {username}! You are now logged in.")
                print("Session user_id:", request.session.get('user_id'))
                return redirect('bank_account')
            except User.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def bank_account(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'You need to log in to access your bank account.')
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('login')

    return render(request, 'bank_account.html', {'user': user})
