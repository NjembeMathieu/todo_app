# car_prediction/urls.py
from django.urls import path
from . import views

app_name = 'car_prediction'

urlpatterns = [
    path('', views.car_prediction_home, name='home'),
    path('predict/', views.predict_car_price, name='predict'),
    path('batch/', views.batch_prediction, name='batch_predict'),
]