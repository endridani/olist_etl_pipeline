"""back_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers

from data_mart.views import CustomersViewSet, SellersViewSet, ProductsViewSet

router = routers.SimpleRouter()
router.register(r'dim_customers', CustomersViewSet)
router.register(r'dim_sellers', SellersViewSet)
router.register(r'dim_products', ProductsViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('', include('source_olist_data.urls')),
]
