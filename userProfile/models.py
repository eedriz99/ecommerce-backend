from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, firstname, lastname, password=None, **kwargs):
        if not email:
            raise ValueError('A valid and unique e-mail address is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, firstname=firstname,
                          lastname=lastname, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, password=None, **kwargs):
        user = self.create_user(email, firstname, lastname, password, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(
        max_length=255, primary_key=True, unique=True, verbose_name='E-mail address')
    firstname = models.CharField(max_length=50, verbose_name='First name')
    lastname = models.CharField(max_length=50, verbose_name='Last name')
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=10, null=True, blank=True)

    zipcode = models.CharField(
        max_length=6,
        verbose_name="Zip Code/ Postal Address",
        help_text="Enter your Zip Code or Postal Address",
        null=True, blank=True)
    country = models.CharField(
        max_length=10, default="USA", null=True, blank=True)
    picture = models.ImageField(
        upload_to="profilePictures/", null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['firstname', 'lastname']

    @property
    def is_staff(self):
        return self.is_admin

    # @property
    # def get_email(self):
    #     try:
    #         return self.email
    #     except AttributeError:
    #         return "The object has no  attribute `email`."

    def get_full_name(self):
        return f"{self.firstname} {self.lastname}"

    def get_short_name(self):
        return self.firstname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email
