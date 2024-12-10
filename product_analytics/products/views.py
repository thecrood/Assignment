from django.db.models import Avg, Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from django.db import models
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ProductAnalyticsView(APIView):
    @method_decorator(cache_page(60 * 5)) 
    def get(self, request):
        category = request.GET.get('category', '').lower()
        min_price = float(request.GET.get('min_price', 0))
        max_price = float(request.GET.get('max_price', float('inf')))

        # Filtering
        products = Product.objects.filter(
            category__iexact=category,
            price__gte=min_price,
            price__lte=max_price,
        )

        # Aggregation
        total_products = products.count()
        average_price = products.aggregate(Avg('price'))['price__avg'] or 0
        total_stock_value = products.aggregate(total_value=Sum(models.F('price') * models.F('stock')))['total_value'] or 0

        return Response({
            'total_products': total_products,
            'average_price': average_price,
            'total_stock_value': total_stock_value,
        })
