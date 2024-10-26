from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Min, Max
from .models import Info, Prices, Financials
from .serializers import InfoSerializer, PricesSerializer, FinancialsSerializer
from rest_framework.decorators import action

class InfoViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Info.objects.all()
        
        # Existing filters
        symbols = request.query_params.getlist('symbols[]', [])
        if symbols:
            queryset = queryset.filter(symbol__in=symbols)
            
        sectors = request.query_params.getlist('sectors[]', [])
        if sectors:
            queryset = queryset.filter(gics_sector__in=sectors)
            
        sub_industries = request.query_params.getlist('subIndustries[]', [])
        if sub_industries:
            queryset = queryset.filter(gics_sub_industry__in=sub_industries)
        
        # New location filter
        locations = request.query_params.getlist('locations[]', [])
        if locations:
            queryset = queryset.filter(headquarters_location__in=locations)
            
        # Founded range filter
        founded_min = request.query_params.get('founded_min')
        founded_max = request.query_params.get('founded_max')
        if founded_min:
            queryset = queryset.filter(founded__gte=founded_min)
        if founded_max:
            queryset = queryset.filter(founded__lte=founded_max)
            
        serializer = InfoSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """Return unique values for different fields to populate filters"""
        founded_range = Info.objects.aggregate(
            min_founded=Min('founded'),
            max_founded=Max('founded')
        )
        return Response({
            'symbols': list(Info.objects.values_list('symbol', flat=True).distinct().order_by('symbol')),
            'sectors': list(Info.objects.values_list('gics_sector', flat=True).distinct().order_by('gics_sector')),
            'subIndustries': list(Info.objects.values_list('gics_sub_industry', flat=True).distinct().order_by('gics_sub_industry')),
            'locations': list(Info.objects.values_list('headquarters_location', flat=True).distinct().order_by('headquarters_location')),
            'founded_range': {
                'min': founded_range['min_founded'],
                'max': founded_range['max_founded']
            }
        })

class PricesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Prices.objects.all()
        
        # Symbol filter
        symbols = request.query_params.getlist('symbols[]', [])
        if symbols:
            queryset = queryset.filter(ticker__in=symbols)
            
        # Metric filter
        metrics = request.query_params.getlist('metrics[]', [])
        if metrics:
            queryset = queryset.filter(metric__in=metrics)
            
        # Date range filter
        date_min = request.query_params.get('date_min')
        date_max = request.query_params.get('date_max')
        if date_min:
            queryset = queryset.filter(date__gte=date_min)
        if date_max:
            queryset = queryset.filter(date__lte=date_max)
        
        limit = request.query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except (ValueError, TypeError):
                pass
                
        serializer = PricesSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """Return available filter options"""
        date_range = Prices.objects.aggregate(
            min_date=Min('date'),
            max_date=Max('date')
        )
        return Response({
            'metrics': list(Prices.objects.values_list('metric', flat=True).distinct().order_by('metric')),
            'date_range': {
                'min': date_range['min_date'],
                'max': date_range['max_date']
            }
        })

class FinancialsViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = Financials.objects.all()
            
            # Symbol filter
            symbols = request.query_params.getlist('symbols[]', [])
            if symbols:
                queryset = queryset.filter(ticker__in=symbols)
                
            # Variable filter
            variables = request.query_params.getlist('variables[]', [])
            if variables:
                queryset = queryset.filter(variable__in=variables)
                
            # Date range filter
            date_min = request.query_params.get('date_min')
            date_max = request.query_params.get('date_max')
            if date_min:
                queryset = queryset.filter(date__gte=date_min)
            if date_max:
                queryset = queryset.filter(date__lte=date_max)
                
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

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        """Return available filter options"""
        date_range = Financials.objects.aggregate(
            min_date=Min('date'),
            max_date=Max('date')
        )
        return Response({
            'variables': list(Financials.objects.values_list('variable', flat=True).distinct().order_by('variable')),
            'date_range': {
                'min': date_range['min_date'],
                'max': date_range['max_date']
            }
        })
