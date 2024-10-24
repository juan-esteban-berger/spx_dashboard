from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InfoViewSet, PricesViewSet, FinancialsViewSet

router = DefaultRouter()
router.register(r'info', InfoViewSet)
router.register(r'prices', PricesViewSet)
router.register(r'financials', FinancialsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
