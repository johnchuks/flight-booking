from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from account.manager import AirtechUserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=80, blank=True, null=True)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    email = models.EmailField(blank=True, unique=True, null=True)
    profile_photo = models.ImageField(upload_to='account_photos/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AirtechUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'password']

    
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower().strip()
        
        super(User, self).save(*args, **kwargs);

    @property
    def is_admin(self):
        """
        Is the user an admin
        """
        return self.is_staff


def get_user(pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return ("User does not exist")
    return user
