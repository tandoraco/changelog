def super_user_and_admin(user):
    return user.is_admin and user.is_superuser and user.is_active
