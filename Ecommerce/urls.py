"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from app import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.product_list,name='home'),
    path('home/<int:id>',views.product_list,name='home'),
    path('product_details/<int:pk>',views.product_details,name='product_details'),
    path('registration/', views.Customerregistration.as_view(), name="registration"),
    path("login/", views.userlogin, name="login"),
    path('Add_Address/',views.profile.as_view(),name='Add_Address'),
    path('address/',views.address,name='address'),
    path('updateaddress/<int:id>/',views.updateAddress,name='updateaddress'),
    path('add_to_cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('show_cart/',views.show_cart,name='show_cart'),
    path('plus_cart/',views.plus_cart,name='plus_cart'),
    path('minus_cart/',views.minus_cart,name='minus_cart'),
    path('remove/',views.remove,name='remove'),
    path('checkout/',views.checkout,name='checkout'),
    path('paymentdone/',views.paymentdone),
    path('logout/',views.logout_user,name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist_page/',views.wishlist_view,name='wishlist_page'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('profile/',views.profile1,name='profile')
    # path('checkoutrender',views.checkoutrender,name='checkoutrender')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
