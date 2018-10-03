"""foodpro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from foodapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^user/',include('foodapp.urls')),
    url(r'^restaurant/$',views.register_restaurant,name='register_restaurant'),
    url(r'^restaurant/login/$',views.login_restaurant,name='login_restaurant'),
    url(r'^restaurant/mainpage/$',views.mainpage_restaurant,name='mainpage_restaurant'),
    url(r'^restaurant/menu/$',views.menu_restaurant,name='menu_restaurant'),
    url(r'^restaurant/rating/$',views.rating_restaurant,name='rating_restaurant'),
    url(r'^restaurant/logout/$',views.logout_restaurant,name='logout_restaurant'),

    url(r'^restaurant/editprofile/$',views.editprofile_restaurant,name='editprofile_restaurant'),

    url(r'^restaurant/addmenu/$',views.addmenu,name='addmenu'),
    url(r'^restaurant/editmenu/$',views.editmenu,name='editmenu'),
    url(r'^restaurant/deletemenu/(?P<id>\d+)/$',views.deletemenu,name='deletemenu'),

    url(r'^restaurant/deleteorder/$',views.deleteorder,name='deleteorder'),

]
