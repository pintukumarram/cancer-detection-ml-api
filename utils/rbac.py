from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def roles_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in allowed_roles:
                flash("You do not have permission to access that page.")
                return redirect(url_for("common_routes.profile"))
            return view_func(*args, **kwargs)

        return wrapped

    return decorator
