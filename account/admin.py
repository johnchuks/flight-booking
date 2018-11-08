from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from account.forms import AirtechUserCreationForm, AirtechUserChangeForm
# Register your models here.

@admin.register(User)
class AirtechUser(UserAdmin):
    model = User
  
    fieldsets = (
      (None, {'fields': ('email', 'password')}),
      (_('Personal info'), {'fields': ('first_name', 'last_name')}),
      (_('Permissions'), {'fields': ('is_admin', 'is_superuser',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password'),
        }),
    )
    form = AirtechUserChangeForm
    add_form = AirtechUserChangeForm
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_admin')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name', 'email')
