from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "bio",
        "profile_pic",
        "is_staff",
        "is_superuser",
    )
    list_editable = ("email", "bio", "profile_pic", "is_staff", "is_superuser")


admin.site.register(User, UserAdmin)
