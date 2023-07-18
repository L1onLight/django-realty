from django.shortcuts import redirect


def logout_required(view_func):
    """Redirects to the home page by name in urls.py if user authenticated"""

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper


def login_required_my(view_func):
    """Redirects to the home page by name in urls.py if user is not authenticated"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


def agent_only(view_func):
    """Redirects to the home page if request.user is not agent or staff. If user not is_authenticated,
    returns redirect to login page"""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.agent or not request.user.is_staff:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper
