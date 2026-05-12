from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('ru/', views.main_ru, name='main_ru'),
    path('popitka/', views.popitka, name='popitka'),
    path('api/leetcode/', views.leetcode_stats, name='leetcode_stats'),
]