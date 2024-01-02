from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(item)
admin.site.register(Person)
admin.site.register(Product)
admin.site.register(CartItem)