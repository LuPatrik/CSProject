from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm, LoginForm
from django.db import connection, transaction
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal

def index(request):
    return render(request, "index.html")

#vulnerable register
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("users password is saved as:",password)
            User.objects.create(username=username, password=password)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

#vulnerable login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username, password=password)
                request.session['user_id'] = user.id
                return redirect('bank_account')
            except User.DoesNotExist:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
"""
#safe register
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            encrypted_password = make_password(password)
            print("users password is saved as:", encrypted_password)

            User.objects.create(username=username, password=encrypted_password)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

#safe login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)

                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    return redirect('bank_account')
                else:
                    return redirect('login')
            except User.DoesNotExist:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
"""
def bank_account(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("login")
    response = render(request, "bank_account.html", {"user": user})
    #to prevent users from going back after another user has logged out
    #response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    #response['Pragma'] = 'no-cache'
    return response


def logout(request):
    request.session.flush()
    return redirect('login')

def search_users(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    search_query = request.GET.get('q', '')
    users = []

    #unsafe query
    if search_query:
        raw_query = f"SELECT username FROM bank_user WHERE username LIKE '%{search_query}%'"
        with connection.cursor() as cursor:
            cursor.execute(raw_query)
            results = cursor.fetchall()
        users = results
    #safe query:
    #if search_query:
    #    users = User.objects.filter(username__icontains=search_query).values_list('username', flat=True)

    return render(request, 'bank_account.html', {
        'user': user,
        'users': users,
        'query': search_query,
    })

@transaction.atomic
def transfer_money(request):
    if request.method == 'POST':
        sender_id = request.session.get('user_id')
        recipient_username = request.POST.get('recipient')
        amount = request.POST.get('amount')

        if not sender_id:
            return redirect('login')

        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            return redirect('bank_account')

        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return redirect('bank_account')

        try:
            amount = Decimal(amount)
            if amount <= 0:
                return redirect('bank_account')
        except (ValueError, Decimal.InvalidOperation):
            return redirect('bank_account')

        if sender.balance < amount:
            return redirect('bank_account')

        
        sender.balance -= amount
        recipient.balance += amount
        sender.save()
        recipient.save()
        return redirect('bank_account')

    return redirect('bank_account')