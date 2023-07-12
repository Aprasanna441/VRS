from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager 
from django.core.validators import FileExtensionValidator
from datetime import datetime, timedelta
import datetime
import pytz
from django.utils import timezone
utc=pytz.UTC
from django.core.validators import MaxValueValidator, MinValueValidator


class District(models.Model):
    name = models.CharField(unique=True,max_length=100)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    name = models.CharField(unique=True,max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()

        # Check if the municipality belongs to the correct district
        if self.district and self.district != self.district_id:
            print("galat info")
            raise ValidationError("Municipality is not in the correct district.")
    
muni=['Bhaktapur','Suryavinayak','Changunarayan']
metro=['Kathmandu','Bharatpur','Butwal']

class Ward(models.Model):
    number = models.IntegerField()
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)
    
    def clean(self):
        # Validate the ward number based on the municipality
        if self.municipality_id:
            municipality = Municipality.objects.get(id=self.municipality_id)
            print(municipality)
            if municipality.name in muni  and self.number > 9:
                raise ValidationError("Invalid ward number for Municipality1. It should be less than or equal to 9.")
            elif municipality.name  in metro and self.number > 32:
                raise ValidationError("Invalid ward number for Municipality2. It should be less than or equal to 32.")
    

    



class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
class Citizen(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200)
    nin_no=models.CharField(max_length=30,null=True,blank=True)
    photo=models.ImageField(upload_to='user_photos',null=True,blank=True)
    district =models.ForeignKey(District,blank=True,null=True,on_delete=models.CASCADE)
    local_body=models.ForeignKey(Municipality,blank=True,null=True,on_delete=models.CASCADE)
    ward_no=models.IntegerField(blank=True,null=True)
    joined_on=models.DateTimeField(auto_now_add=True)
    phone=models.CharField(max_length=15,blank=True,null=True)
    identification = models.FileField(upload_to='identities', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])],null=True,blank=True)

    def __str__(self):
        return self.full_name
    
    def clean(self):
        # Validate the ward number based on the municipality
        if self.local_body_id:
            municipality = Municipality.objects.get(id=self.local_body_id)
            print(municipality)
            if municipality.name in muni  and self.ward_no > 9:
                raise ValidationError("Invalid ward number for municipality. It should be less than or equal to 9.")
            elif municipality.name  in metro and self.ward_no > 32:
                raise ValidationError("Invalid ward number for Metro. It should be less than or equal to 32.")
    

class Brand(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name


VEHICLE_TYPE=(
    ('Two Wheeler','Two Wheeler'),
    ('Four Wheeler','Four Wheeler'),
    
)


    
class Vehicle(models.Model):
   
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    manufactured_date=models.DateField()
    identity_number=models.CharField(max_length=200)
    engine_capacity=models.IntegerField(MinValueValidator(1))
    vehicle_type=models.CharField(choices=VEHICLE_TYPE,default=None,max_length=30)


    def __str__(self):
        return str(self.identity_number)
    

    
class  RegisteredVehicle(models.Model):
    number = models.CharField(max_length=20)
    owner=models.ForeignKey(Citizen,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    registered_at=models.DateField(auto_now_add=True)
    bluebook=models.FileField(upload_to='bluebook_pics')
    registration_certificate=models.ImageField( upload_to='registration_certificates')
    renewed_date=models.DateTimeField(blank=True,null=True)
    is_approved=models.BooleanField(default=False)
    
    
    
    @property
    def expiry_date(self):
        time=timedelta(days=12)
        return self.renewed_date + time
    
    @property
    def number(self):
        return  self.owner
    
    @property
    def expired(self):
        if timezone.now().replace(tzinfo=utc) > self.expiry_date.replace(tzinfo=utc):
            return "Yes"
        else:
            return "No"
        
    @property
    def timeremaining(self):
        return self.expiry_date.replace(tzinfo=utc)-timezone.now()
    
    
    @property
    def total(self):
        if self.vehicle.engine_capacity<1000:
            return 1000
        else:
            return 1500
    
    def __str__(self):
        return self.number
    
    

class Transactions(models.Model):
    vehicle=models.ForeignKey(RegisteredVehicle,on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True)
    amount=models.BigIntegerField()


    def __str__(self):
        return self.time
    





    

    
    

    


    
