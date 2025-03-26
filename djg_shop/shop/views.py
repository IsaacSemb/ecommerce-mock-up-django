from django.shortcuts import render, HttpResponse
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func

from .models import Order, OrderItem, Product, Customer

def product_list(request):
    return HttpResponse('ok')