from django.urls import path
from .views import ProductAnalyticsView

urlpatterns = [
    path('analytics/', ProductAnalyticsView.as_view(), name='product-analytics'),
]
