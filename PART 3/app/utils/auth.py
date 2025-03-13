from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.services.user import UserService

def admin_required():
    """Decorator to require admin privileges."""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user_service = UserService()
            user = user_service.get(current_user_id)
            
            if not user or not user.is_admin:
                return jsonify({"msg": "Admin access required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def get_current_user():
    """Get the current authenticated user."""
    current_user_id = get_jwt_identity()
    user_service = UserService()
    return user_service.get(current_user_id)

def is_admin():
    """Check if current user is admin."""
    user = get_current_user()
    return user and user.is_admin 