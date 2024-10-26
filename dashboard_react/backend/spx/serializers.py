from rest_framework import serializers
from .models import Info, Prices, Financials
import math

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('symbol', 'security', 'gics_sector', 'gics_sub_industry', 
                 'headquarters_location', 'date_added', 'cik', 'founded')

class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('date', 'ticker', 'metric', 'value')

class FinancialsSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Financials
        fields = ('ticker', 'date', 'variable', 'value')

    def get_value(self, obj):
        if obj.value is None:
            return None
        if math.isnan(obj.value) or math.isinf(obj.value):
            return None
        return obj.value
