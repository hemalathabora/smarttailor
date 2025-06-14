from django.contrib import admin
from .models import  Customer, Tailor, Fabric, Measurement, Order


admin.site.register(Customer)
admin.site.register(Tailor)
admin.site.register(Fabric)
admin.site.register(Measurement)
admin.site.register(Order)
