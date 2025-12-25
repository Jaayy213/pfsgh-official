from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import UserRegistrationForm, LoginForm


def register_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            if request.user.is_staff or request.user.is_superuser:
                return redirect("blog_dashboard")

            if next_url:
                if url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                    return redirect(next_url)

            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
            "next": next_url,
        },
    )


def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data["user"])

            if request.user.is_staff or request.user.is_superuser:
                return redirect("blog_dashboard")

            if next_url:
                if url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                    return redirect(next_url)

            return redirect("home")
    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": next_url,
        },
    )


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


@permission_required('accounts.view_user', raise_exception=True)
def admin_only_view(request):
    return render(request, "accounts/admin_only.html")
