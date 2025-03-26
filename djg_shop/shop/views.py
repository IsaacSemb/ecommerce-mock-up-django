from django.shortcuts import render, HttpResponse
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderItem, Product, Customer

@api_view()
def product_list(request):
    return Response('ok')
