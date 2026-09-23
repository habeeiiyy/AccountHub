from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache 
from .forms import Loginform 
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
@never_cache 
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect("Accounts:home")

    if request.method=="POST":
        form=Loginform(request.POST)

        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]

            user=authenticate(
                        request,
                        username=username,
                        password=password
                    )
            if user is not None:
                login(request,user)
                return redirect("Accounts:home")
            form.add_error(None,"invalid username or password")
    else:
        form=Loginform()
    return render (
        request,"Accounts/login.html",{"form":form}
    )
@never_cache
@login_required
def home(request):
    return render(request,"Accounts/home.html")

@never_cache
@require_POST
def logout_view(request):
    logout(request)
    return redirect("Accounts:login")

@never_cache
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("Accounts:home")

    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Accounts:login")
    else:
        form=UserCreationForm()
    return render(request,"Accounts/signup.html",{"form":form})