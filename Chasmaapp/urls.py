from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.product_list, name='product_list'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
     path('logout/', views.logout, name="logout"), 
    path('offer', views.offer, name='offer'),
    path('thankyou/', views.thankyou, name='thankyou'),
    
]

