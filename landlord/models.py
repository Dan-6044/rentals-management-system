from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class LandlordManager(BaseUserManager):
    def create_landlord(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        landlord = self.model(name=name, email=email, **extra_fields)
        landlord.set_password(password)
        landlord.save(using=self._db)
        return landlord

class Landlord(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='landlord_profiles/')
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = LandlordManager()

    def __str__(self):
        return self.name


from django.contrib.auth.models import User

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=255)
    layout = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()  # Add latitude
    longitude = models.FloatField()  # Add longitude
    features = models.TextField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    agency = models.CharField(max_length=255, blank=True)
    amenities = models.TextField()
    terms = models.TextField()
    contact = models.CharField(max_length=255)
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return self.property_name

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

class PropertyVideo(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='property_videos/')