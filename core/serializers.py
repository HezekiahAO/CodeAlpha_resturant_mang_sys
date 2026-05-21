from rest_framework import serializers
from .models import Category, MenuItem, Table, Reservation, Order, OrderItem, Inventory, Payment


# Translation to/from JSON


# ─── MENU ───────────────────────────────────────────────
class CategorySerializer(serializers.ModelSerializer):
    # Why ModelSerializer? It automatically generates fields
    # from the model so we don't have to define them manually
    class Meta:
        model = Category
        fields = '__all__'  # include every field from the model


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


# ─── TABLES ─────────────────────────────────────────────
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


# ─── RESERVATIONS ───────────────────────────────────────
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


# ─── ORDERS ─────────────────────────────────────────────
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # Why nested? So when you fetch an order, you see the actual
    # items inside it, not just their IDs
    items = OrderItemSerializer(many=True, read_only=True)

    # Why SerializerMethodField? get_total() is a method on the model, not a real DB column, this is how we expose it in the API
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_total(self, obj):
        return obj.get_total()


# ─── INVENTORY ──────────────────────────────────────────
class InventorySerializer(serializers.ModelSerializer):
    # Why SerializerMethodField again? is_low() is also a method
    # not a DB column, same pattern as get_total()
    is_low = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = '__all__'

    def get_is_low(self, obj):
        return obj.is_low()


# ─── PAYMENTS ───────────────────────────────────────────
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'