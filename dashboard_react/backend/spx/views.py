from rest_framework import viewsets
from .models import Info, Prices, Financials
from .serializers import InfoSerializer, PricesSerializer, FinancialsSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer

class PricesViewSet(viewsets.ModelViewSet):
    queryset = Prices.objects.all()
    serializer_class = PricesSerializer
    
    @action(detail=False, methods=['get'])
    def by_ticker(self, request):
        ticker = request.query_params.get('ticker', None)
        if ticker:
            prices = self.queryset.filter(ticker=ticker)
            serializer = self.get_serializer(prices, many=True)
            return Response(serializer.data)
        return Response({'error': 'Ticker parameter is required'})

class FinancialsViewSet(viewsets.ModelViewSet):
    queryset = Financials.objects.all()
    serializer_class = FinancialsSerializer
