from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from source_olist_data import views

urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('customers/', views.CustomersList.as_view()),
    path('sellers/', views.SellersList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
