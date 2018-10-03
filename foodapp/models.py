from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user=models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)
    name=models.CharField(max_length=256)
    mobile=models.CharField(max_length=20)
    address=models.CharField(max_length=512)
    pincode=models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class RestaurantProfileInfo(models.Model):
    user=models.OneToOneField(User,related_name='restaurant_profile',on_delete=models.CASCADE)
    restaurant_name=models.CharField(max_length=64,blank=True)
    restaurant_mobile=models.CharField(max_length=20)
    restaurant_address=models.CharField(max_length=512,blank=True)
    restaurant_pincode=models.IntegerField()
    restaurant_starttime=models.TimeField(null=True)
    restaurant_endtime=models.TimeField(null=True)
    restaurant_avgrating=models.DecimalField(default=0,decimal_places=1,max_digits=2)
    restaurant_noofrating=models.IntegerField(default=0)
    restaurant_nooforder=models.IntegerField(default=0)
    restaurant_noofmenu=models.IntegerField(default=0)

    def __str__(self):
        return self.restaurant_name

class RestaurantMenu(models.Model):
    restaurant=models.ForeignKey(RestaurantProfileInfo,related_name='restaurant_menu',on_delete=models.CASCADE)
    dish=models.CharField(max_length=32)
    dish_description=models.CharField(max_length=256)
    dish_price=models.IntegerField()
    category=models.CharField(max_length=16)
    availability=models.BooleanField(default=True)
    speciality=models.BooleanField(default=False)

    def __str__(self):
        return self.dish

class Rating(models.Model):
    rating_user=models.ForeignKey(UserProfileInfo,related_name='rating',on_delete=models.CASCADE)
    rating_restaurant=models.ForeignKey(RestaurantProfileInfo,related_name='rating')
    rating_value=models.IntegerField()
    rating_description=models.CharField(max_length=256)
    rating_at=models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    order_user=models.ForeignKey(UserProfileInfo,related_name='order',on_delete=models.CASCADE)
    order_dish=models.ForeignKey(RestaurantMenu,related_name='order')
    quantity=models.IntegerField()
    order_at=models.DateTimeField(auto_now_add=True)
    delivered=models.BooleanField(default=False)
