from django.urls import path
from . import views  

urlpatterns = [
    path('', views.home, name="Home"),
    path('get_stock/<str:stock_name>/', views.get_stock, name="get_stock"),
]
