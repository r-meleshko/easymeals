from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view

from .forms import LoginForm


User = get_user_model()


@api_view(['GET', 'POST'])
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Save session as cookie to login the user
                login(request, user)
                return redirect('recipes:choose')
            else:
                # Incorrect credentials
                return render(request, 'accounts/login.html',
                              {'error_message': 'You have entered an invalid username or password',
                               'form': form})
        else:
            form = LoginForm()
            return render(request, 'accounts/login.html', {'error_message': "Invalid CAPTCHA", 'form': form})

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
