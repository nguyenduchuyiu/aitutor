from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from lessons.models import Lesson

@login_required(login_url='/login/')  # Redirect to login page if not logged in
def home(request):
    lessons = Lesson.objects.all()
    return render(request, "home.html", {"lessons": lessons})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or dashboard after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

@login_required(login_url='/login/')  # Ensure user is logged in to logout
def logout_view(request):
    logout(request)  # Log the user out
    request.session.flush()  # Clear all session data
    messages.success(request, 'You have been logged out successfully.')  # Optional: Add a success message
    return redirect('/login/')  # Redirect to the login page after logout

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def index_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')  
    else:
        return redirect('login')  