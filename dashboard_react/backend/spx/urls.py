from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InfoViewSet, PricesViewSet, FinancialsViewSet

router = DefaultRouter()
router.register(r'info', InfoViewSet, basename='info')
router.register(r'prices', PricesViewSet, basename='prices')
router.register(r'financials', FinancialsViewSet, basename='financials')

urlpatterns = [
    path('', include(router.urls)),
]
