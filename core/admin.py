from django.contrib import admin
from .models import Category, MenuItem, Table, Reservation, Order, OrderItem, Inventory, Payment
# Register your models here.

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Inventory)
admin.site.register(Payment)