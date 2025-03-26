from django.shortcuts import render
from django.db.models.aggregates import Count, Avg, Max, Min, Sum
from django.db.models import Value, F, Func

from .models import Order, OrderItem, Product, Customer

def playground(request):
    
    object_by_id = Product.objects.filter(id=1200).exists()
    
        
    context = {
        
        
        # annotates adds new fields to a model
        'pdt_filter_18': Customer.objects
        .annotate(
            
            full_name = Func(
                F('first_name'), 
                Value(' ') , 
                F('last_name'),
                function = 'CONCAT'
                
                )
            
            ),
        
        # annotates adds new fields to a model
        'pdt_filter_17': Customer.objects
        .annotate(
            
            full_name = Func(
                F('first_name'), 
                Value(' ') , 
                F('last_name'),
                function = 'CONCAT'
                
                )
            
            ),
        
        'pdt_filter_16': Product.objects
        .aggregate( 
                    num_of_ids = Count('id'), # this counts non null records of field 
                    maximum_price = Max('unit_price') # this is used numerical values
                ), 
        
        'pdt_filter_15':Order.objects
        .select_related('customer')
        .prefetch_related('orderitem_set__product')
        .order_by('-created_at')[:5],
        
        
        # getting objects not dictionaries or tuples
        'pdt_filter_14': Product.objects
        .only('id','product_name', 'category', 'category__category_name')[:10],
        
        # exrecise: products that have been ordered sorted by title
        'pdt_filter_13': Product.objects
        .filter( id__in = OrderItem.objects.values('product'))
        .order_by('product_name'),
        
        # choosing select field to query / foreign fields too <home__foreign> (tuples edition)
        'pdt_filter_12': Product.objects
        .values_list('id','product_name', 'category')[:5],
        
        # choosing select field to query / foreign fields too <home__foreign>
        'pdt_filter_11': Product.objects
        .values('id','product_name', 'category', 'category__category_name')[:5],
        
        # contains insensitive (UNDONE)
        'pdt_filter_10': Product.objects
        .filter(unit_price__lte=2),
        
        # contains case sensitive (UNDONE)
        'pdt_filter_9': Product.objects
        .filter(unit_price__lte=2),
        
        # ends with insenstive (UNDONE)
        'pdt_filter_8': Product.objects
        .filter(unit_price__lte=2),
        
        # ends with case sensitive (UNDONE)
        'pdt_filter_7': Product.objects
        .filter(unit_price__lte=2),
        
        # starts with insensitive (UNDONE)
        'pdt_filter_6': Product.objects
        .filter(product_name__istartswith='a'),
        
        # starts with case sensitive
        'pdt_filter_5': Product.objects
        .filter(product_name__startswith='A'),
        
        # less than or equal
        'pdt_filter_4': Product.objects
        .filter(unit_price__lte=2),
        
        # less than 
        'pdt_filter_3': Product.objects
        .filter(unit_price__lt=2),
        
        # greater than or equal to
        'pdt_filter_2': Product.objects
        .filter(unit_price__gte=99),
        
        # greater than and less than
        'pdt_filter_1': Product.objects
        .filter(unit_price__gt=99),
        
        # getting by id
        'object_by_id':  object_by_id,
        
        # querying objects from db and slicing them
        'all_products':Product.objects.all()[:5],
        
    }
    

    return render(request, 'playground.html', context)