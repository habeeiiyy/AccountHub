from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import AdminUserForm, LoginForm

User = get_user_model()


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


staff_required = user_passes_test(is_staff_user, login_url="Accounts:admin_login")


def get_admin_return_url(request):
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return reverse("Accounts:admin_dashboard")


@never_cache
def login_view(request):

    if request.user.is_authenticated:
        return redirect("Accounts:home")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Accounts:home")
            form.add_error(None, "invalid username or password")
    else:
        form = LoginForm()
    return render(request, "Accounts/login.html", {"form": form})


@never_cache
@login_required
def home(request):
    return render(request, "Accounts/home.html")


@never_cache
@require_POST
def logout_view(request):
    logout(request)
    return redirect("Accounts:login")


@never_cache
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("Accounts:home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Accounts:login")
    else:
        form = UserCreationForm()
    return render(request, "Accounts/signup.html", {"form": form})


@never_cache
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("Accounts:admin_dashboard")
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect("Accounts:admin_dashboard")
            form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "Accounts/admin_login.html", {"form": form})


@never_cache
@staff_required
def admin_dashboard(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.all().order_by("id")

    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "Accounts/admin_dashboard.html",
        {"users": page_obj, "query": query, "page_obj": page_obj},
    )


@never_cache
@staff_required
def user_form(request, user_id=None):
    user = get_object_or_404(User, id=user_id) if user_id is not None else None
    form_data = request.POST if request.method == "POST" else None
    form = AdminUserForm(form_data, instance=user)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("Accounts:admin_dashboard")

    title = "Edit User" if user else "Add User"
    return render(
        request,
        "Accounts/admin_user_form.html",
        {"form": form, "title": title},
    )


@never_cache
@require_POST
@staff_required
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()

    return redirect(get_admin_return_url(request))


@never_cache
@require_POST
@staff_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        user.delete()

    return redirect(get_admin_return_url(request))
