from rest_framework import viewsets
from rest_framework.response import Response
from .models import Info, Prices, Financials
from .serializers import InfoSerializer, PricesSerializer, FinancialsSerializer
from rest_framework.decorators import action

class InfoViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Info.objects.all()
        
        # Filter by symbols (multiple)
        symbols = request.query_params.getlist('symbols[]', [])
        if symbols:
            queryset = queryset.filter(symbol__in=symbols)
            
        # Filter by sectors (multiple)
        sectors = request.query_params.getlist('sectors[]', [])
        if sectors:
            queryset = queryset.filter(gics_sector__in=sectors)
            
        # Filter by sub industries (multiple)
        sub_industries = request.query_params.getlist('subIndustries[]', [])
        if sub_industries:
            queryset = queryset.filter(gics_sub_industry__in=sub_industries)
            
        serializer = InfoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """Return unique values for different fields to populate filters"""
        return Response({
            'symbols': list(Info.objects.values_list('symbol', flat=True).distinct().order_by('symbol')),
            'sectors': list(Info.objects.values_list('gics_sector', flat=True).distinct().order_by('gics_sector')),
            'subIndustries': list(Info.objects.values_list('gics_sub_industry', flat=True).distinct().order_by('gics_sub_industry')),
        })

class PricesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Prices.objects.all()
        
        # Filter by symbols (multiple)
        symbols = request.query_params.getlist('symbols[]', [])
        if symbols:
            queryset = queryset.filter(ticker__in=symbols)
        
        limit = request.query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except (ValueError, TypeError):
                pass
                
        serializer = PricesSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def by_ticker(self, request):
        ticker = request.query_params.get('ticker')
        if ticker:
            queryset = Prices.objects.filter(ticker=ticker)
            limit = request.query_params.get('limit')
            if limit:
                try:
                    limit = int(limit)
                    queryset = queryset[:limit]
                except (ValueError, TypeError):
                    pass
            serializer = PricesSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({'error': 'Ticker parameter is required'})

class FinancialsViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = Financials.objects.all()
            
            # Filter by symbols (multiple)
            symbols = request.query_params.getlist('symbols[]', [])
            if symbols:
                queryset = queryset.filter(ticker__in=symbols)
                
            limit = request.query_params.get('limit')
            if limit:
                try:
                    limit = int(limit)
                    queryset = queryset[:limit]
                except (ValueError, TypeError):
                    pass
                    
            serializer = FinancialsSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error processing financials request: {str(e)}")
            return Response([])
