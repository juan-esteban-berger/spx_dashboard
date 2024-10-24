from rest_framework import serializers
from .models import Info, Prices, Financials

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'

class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = '__all__'

class FinancialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financials
        fields = '__all__'
