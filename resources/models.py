from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator

class Company(models.Model):
    name = models.CharField(
        max_length=100, 
        help_text='company name',
        unique=True
    )
    established_date = models.DateField(auto_now=True)
    industry = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(
        max_length=100, 
        verbose_name='email address', 
        unique=True
    )

    def __str__(self):
        return self.name
    

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        to_field='name',
        blank=True, 
        null=True
    )
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    bio = models.TextField(blank=True)
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=True
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.email

    def get_short_name(self):
        return self.email