from django.conf.urls import url
from foodapp import views

app_name='user'

urlpatterns=[
    url(r'^$',views.register_user,name='register_user'),
    url(r'^login/$',views.login_user,name='login_user'),
    url(r'^mainpage/$',views.mainpage_user,name='mainpage_user'),
    url(r'^mainpage/sortdistance/$',views.mainpage_user,name='sortdistance'),
    url(r'^mainpage/sortpopularity',views.mainpage_user,name='sortpopularity'),
    url(r'^orderrestaurant/(?P<id>\d+)/',views.order_from_restaurant,name='order_from_restaurant'),
    #url(r'^mainpage/sortrating',views.mainpage_user,name='sortrating'),
    url(r'^logout/$',views.logout_user,name='logout_user'),


    url(r'^finalizeorder/$',views.finalize_order,name='finalize_order'),

]
