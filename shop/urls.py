from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name = 'register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('collections/', collections, name = 'collections'),
    path('collections/<str:product>', collectionView, name = 'collections'),
    path('collections/<str:cname>/<str:pname>', productDetails, name='collections'),
    path('addtocart/', cart, name='addToCart'),

]