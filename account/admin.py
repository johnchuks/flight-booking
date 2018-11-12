from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from account.forms import AirtechUserChangeForm
from account.models import User


# Register your models here.

@admin.register(User)
class AirtechUser(UserAdmin):
    model = User
  
    fieldsets = (
      (None, {'fields': ('email', 'password')}),
      (_('Personal info'), {'fields': ('first_name', 'last_name', 'profile_photo')}),
      (_('Permissions'), {'fields': ('is_staff', 'is_superuser',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'profile_photo'),
        }),
    )
    form = AirtechUserChangeForm
    add_form = AirtechUserChangeForm
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name', 'email')
