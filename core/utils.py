from django.http import HttpResponseForbidden
from .models import UserProfile

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            profile = UserProfile.objects.get(user=request.user)
            if profile.role.lower() in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to view this page.")
        return _wrapped_view
    return decorator