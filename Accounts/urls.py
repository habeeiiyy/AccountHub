from django.urls import path
from . import views

app_name = "Accounts"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout_view, name="logout"),
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/add/", views.user_form, name="add_user"),
    path("admin-dashboard/<int:user_id>/edit/", views.user_form, name="edit_user"),
    path(
        "admin-dashboard/<int:user_id>/delete/", views.delete_user, name="delete_user"
    ),
    path(
        "admin-dashboard/<int:user_id>/toggle-status/",
        views.toggle_user_status,
        name="toggle_user_status",
    ),
]
