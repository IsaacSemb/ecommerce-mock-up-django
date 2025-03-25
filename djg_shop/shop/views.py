from django.shortcuts import render

from .models import Product

# Create your views here.
def playground(request):
    
    
    context = {
        
        'all_products':Product.objects.all()[:5]
        
    }
    
    
    return render(request, 'playground.html', context)