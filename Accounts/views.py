from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache 


@never_cache 
def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:home")

    if request.method=="POST":
        username=request.POST.get("Username")
        password=request.POST.get("password")

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request,user)
            return redirect("Accounts:home")
        return render(
            request,"Accounts/login.html",
            {"error":"invalid username or password"}
        )
    return render("request","Accounts/login.html")

@never_cache
@login_required
def home(request):
    return render(request,"Accounts/home.html")

@never_cache
def logout_view(request):
    logout(request)
    return redirect("Accounts:login")