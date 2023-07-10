from django.contrib import admin

from .models import CustomUser,District,Municipality,Ward,Citizen,Vehicle,Brand,RegisteredVehicle
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Citizen)
admin.site.register(Municipality)
admin.site.register(District)
admin.site.register(Vehicle)
admin.site.register(Brand)
admin.site.register(RegisteredVehicle)
