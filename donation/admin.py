from django.contrib import admin
from .models import Donor, Receiver, FoodListing, FoodRequest

admin.site.register(Donor)
admin.site.register(Receiver)
admin.site.register(FoodListing)
admin.site.register(FoodRequest)