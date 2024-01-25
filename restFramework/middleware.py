from typing import Any
from .models import Product,User
from django.shortcuts import redirect
import logging
import random


logger=logging.getLogger(__name__)

class PrintProductNamesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This code is executed for each request before the view is called

        # Retrieve all product names and print them to the terminal
        product_names = Product.objects.values_list('name', flat=True)
        print("Product Names:", list(product_names))

        # Call the next middleware in the stack or the view function
        response = self.get_response(request)

        # This code is executed for each response after the view has been processed

        return response
    
class ForceLoginMiddleware:

    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, request):
        logger.debug("Middleware called")
        if not request.user.is_authenticated and request.path_info !=('/users/login/'):
            return redirect('/users/login/')
    
        return self.get_response(request)
    
class RandomNumMiddleware:

    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self, request):
        response=self.get_response(request)

        if request.user.is_authenticated:
            randomnum=random.randint(1000,9999999)
            print(f"Random Number for {request.user.username}: {randomnum}")

        return response

        




        