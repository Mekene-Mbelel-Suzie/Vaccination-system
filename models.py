from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# ======================
# Role model to define user roles
# ======================
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# ======================
# Custom user manager
# ======================
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)

# ======================
# Users model
# ======================
class Users(AbstractUser):
    username = None  # remove username
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    parent_id = models.IntegerField(null=True, blank=True)
    health_cares_id = models.IntegerField(null=True, blank=True)
    hospital_id = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# ======================
# Hospital model
# ======================
class Hospital(models.Model):
    users = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True)
    hospital_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.hospital_name

# ======================
# Parent model
# ======================
class Parent(models.Model):
    users = models.OneToOneField(Users, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    address = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name or self.users.email

# ======================
# Health_cares model
# ======================
class Health_cares(models.Model):
    users = models.OneToOneField(Users, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.full_name or self.users.email