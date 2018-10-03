from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse,resolve
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg,F
from .models import UserProfileInfo,RestaurantProfileInfo,RestaurantMenu,Rating,Order
import json
# Create your views here.
def index(request):
    return HttpResponse("Hellolkfnlwf")

    #return render(request,'index.html',{'test_rankings':test_rankings, 'odi_rankings':odi_rankings, 't20_rankings':t20_rankings,
    #                                    'live_matches':live_matches})

def register_user(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        user=User.objects.create(username=username,password=password,email=email)
        user.set_password(password)
        user.save()

        fullname=request.POST.get('fullname')
        mobile=request.POST.get('mobile')
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        userprofile=UserProfileInfo.objects.create(user=user,name=fullname,mobile=mobile,address=address,pincode=pincode)
        userprofile.save()

        return HttpResponseRedirect(reverse('user:login_user'))
    else:
        return render(request,'signup_user.html')

def login_user(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        try:
            if user and user.profile:
                login(request,user)
                return HttpResponseRedirect(reverse('user:mainpage_user'))
            else:
                return render(request,'login_user.html')
        except:
            return HttpResponse("Invalid Email and password")
    else:
        return render(request,'login_user.html')

def mainpage_user(request):
    if request.user.is_authenticated:
        restaurants=RestaurantProfileInfo.objects.all().order_by('restaurant_avgrating').reverse()

        url_name=resolve(request.path).url_name
        if(url_name is 'sortdistance'):
            user=User.objects.filter(username=request.user.username).first()
            curr_user=user.profile
            curr_user_pincode=int(curr_user.pincode)
            restaurants=list(restaurants)
            n=len(restaurants)
            for i in range(n):
                for j in range(0, n-i-1):
                    if abs(restaurants[j].restaurant_pincode-curr_user_pincode) > abs(restaurants[j+1].restaurant_pincode-curr_user_pincode) :
                        restaurants[j], restaurants[j+1] = restaurants[j+1], restaurants[j]
        elif(url_name is 'sortpopularity'):
            restaurants=RestaurantProfileInfo.objects.order_by('-restaurant_nooforder')

        return render(request,'usermainpage.html',{'restaurants':restaurants})
    else:
        return HttpResponseRedirect(reverse('user:login_user'))

def order_from_restaurant(request,id):
    restaurant=RestaurantProfileInfo.objects.get(id=id)
    ratings=Rating.objects.filter(rating_restaurant=restaurant)
    menus=RestaurantMenu.objects.filter(restaurant=restaurant)
    return render(request,'book.html',{'restaurant':restaurant,'menus':menus,'ratings':ratings})

@csrf_exempt
def finalize_order(request):
    current_user=request.user
    current_userprofile=current_user.profile
    dishes=request.POST.getlist('dishes[]')
    quantities=request.POST.getlist('quantities[]')
    res_id=request.POST.get('res_id')
    print(dishes)
    print(quantities)
    print(res_id)
    res_object=RestaurantProfileInfo.objects.get(id=res_id)
    res_nooforder=res_object.restaurant_nooforder
    for index,item in enumerate(dishes):
        restaurantmenu=RestaurantMenu.objects.filter(dish=item,restaurant__id=res_id)[0]
        res_nooforder=res_nooforder+1
        order=Order.objects.create(order_user=current_userprofile,order_dish=restaurantmenu,quantity=int(quantities[index]))
        order.save()
    res_object.restaurant_nooforder=res_nooforder
    res_object.save()
    payload={'success':True}
    return HttpResponse(json.dumps(payload), content_type='application/json')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login_user'))


#Code included in mainpage_user
#for restaurant in restaurants:
#    rating=Rating.objects.filter(rating_restaurant=restaurant).aggregate(Avg('rating_value'))
#    if(rating['rating_value__avg'] is None):
#        allratings.append('-')
#    else:
#        allratings.append(rating['rating_value__avg'])


#######################################################################################################################################
#######################################################################################################################################
def register_restaurant(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')
        user=User.objects.create(username=username,password=password,email=email)
        user.set_password(password)
        user.save()

        restaurantname=request.POST.get('restaurantname')
        mobile=request.POST.get('mobile')
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        restaurantprofile=RestaurantProfileInfo.objects.create(user=user,restaurant_name=restaurantname,
                                                                restaurant_mobile=mobile,restaurant_address=address,
                                                                restaurant_pincode=pincode)
        restaurantprofile.save()

        return HttpResponseRedirect(reverse('login_restaurant'))
    else:
        return render(request,'signup_restaurant.html')

def login_restaurant(request):
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(username=username,password=password)
            try:
                if user and user.restaurant_profile:
                    login(request,user)
                    return HttpResponseRedirect(reverse('mainpage_restaurant'))
                else:
                    return render(request,'login_restaurant.html')
            except:
                return HttpResponse("Invalid Email and Password")
        else:
            return render(request,'login_restaurant.html')

def logout_restaurant(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_restaurant'))

def mainpage_restaurant(request):
    if request.user.is_authenticated:
        user=User.objects.filter(username=request.user.username).first()
        restaurant=user.restaurant_profile
        orders=Order.objects.filter(order_dish__restaurant=restaurant,delivered=False)
        return render(request,'restprofile.html',{'restaurant':restaurant,'user':user,'orders':orders})
    else:
        return HttpResponseRedirect(reverse('login_restaurant'))

def menu_restaurant(request):
    if request.user.is_authenticated:
        user=User.objects.filter(username=request.user.username).first()
        curr_restaurant=user.restaurant_profile
        menus=RestaurantMenu.objects.filter(restaurant__restaurant_name=curr_restaurant.restaurant_name)
        return render(request,'restmenu.html',{'menus':menus})
    else:
        return HttpResponseRedirect(reverse('login_restaurant'))

def rating_restaurant(request):
    if request.user.is_authenticated:
        user=User.objects.filter(username=request.user.username).first()
        curr_restaurant=user.restaurant_profile
        ratings=Rating.objects.filter(rating_restaurant=curr_restaurant)
        return render(request,'restrate.html',{'ratings':ratings})
    else:
        return HttpResponseRedirect(reverse('login_restaurant'))


@csrf_exempt
def editprofile_restaurant(request):
        name=request.POST["name"];
        address=request.POST["address"];
        pincode=request.POST["pincode"];
        contact=request.POST["contact"];
        starttime=request.POST["starttime"];
        endtime=request.POST["endtime"];

        user=User.objects.filter(username=request.user.username).first()
        curr_restaurant=user.restaurant_profile
        curr_restaurant.restaurant_name=name
        curr_restaurant.restaurant_mobile=contact
        curr_restaurant.restaurant_pincode=pincode
        curr_restaurant.restaurant_address=address
        curr_restaurant.restaurant_starttime=starttime
        curr_restaurant.restaurant_endtime=endtime
        curr_restaurant.save()

        payload={'success':True}
        return HttpResponse(json.dumps(payload), content_type='application/json')



@csrf_exempt
def addmenu(request):
    dish=request.GET['dish']
    description=request.GET['description']
    category=request.GET['category']
    price=request.GET['price']
    user=User.objects.filter(username=request.user.username).first()
    restaurant=user.restaurant_profile
    restaurantmenu=RestaurantMenu.objects.create(restaurant=restaurant,dish=dish,dish_description=description,dish_price=price,category=category)
    restaurantmenu.save()

    payload = {'id':restaurantmenu.id,'dish': dish,'description':description,'price':price,'category':category}
    return HttpResponse(json.dumps(payload), content_type='application/json')

@csrf_exempt
def editmenu(request):
    id=request.GET['id']
    dish=request.GET['dish']
    description=request.GET['description']
    category=request.GET['category']
    price=request.GET['price']

    restaurantmenu=RestaurantMenu.objects.get(id=id)
    restaurantmenu.dish=dish
    restaurantmenu.dish_description=description
    restaurantmenu.dish_price=price
    restaurantmenu.category=category
    restaurantmenu.save()
    payload={'dish':dish,'description':description,'category':category,'price':price}
    return HttpResponse(json.dumps(payload),content_type='application/json')

def deletemenu(request,id):
    restaurantmenu=RestaurantMenu.objects.get(id=id)
    restaurantmenu.delete()
    return HttpResponseRedirect(reverse('menu_restaurant'))

def deleteorder(request):
    id=request.GET['id']
    order=Order.objects.get(id=id)
    order.delivered=True
    order.save()
    payload={'success':True}
    return HttpResponse(json.dumps(payload),content_type='application/json')
