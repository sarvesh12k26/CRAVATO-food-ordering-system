from django.contrib import admin
from .models import UserProfileInfo,RestaurantProfileInfo,RestaurantMenu,Rating,Order
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(RestaurantProfileInfo)
admin.site.register(RestaurantMenu)
admin.site.register(Rating)
admin.site.register(Order)
