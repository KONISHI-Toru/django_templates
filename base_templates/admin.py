from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as bAdmin

@admin.register(User)
class UserAdmin(bAdmin):
    pass

