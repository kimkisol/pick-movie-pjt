from django.contrib import admin
from .models import Basket, Comment, BasketTag

# Register your models here.
admin.site.register(Basket)
admin.site.register(Comment)
admin.site.register(BasketTag)