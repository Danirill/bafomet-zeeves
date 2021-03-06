from django.contrib import admin
from .models import User, UserToken

# Register your models here.

# admin.site.register(User)
admin.site.register(UserToken)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'auth_provider', 'is_confirmed', 'created_at')


admin.site.register(User, UserAdmin)
