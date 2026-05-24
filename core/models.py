from django.db import models
                                   
                                                         # 6 Core Models for Restaurant Management System

# Data Structure and Relationships:
# ─── 1. MENU ────────────────────────────────────────────
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)   #  allows menu items without a category  I got a  category = null  when i ran this
    is_available = models.BooleanField(default=True)
    inventory  = models.ForeignKey('Inventory', on_delete=models.SET_NULL, null=True, blank=True)  # optional link to inventory

    def __str__(self):
        return self.name


# ─── 2. TABLES ──────────────────────────────────────────
class Table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied',  'Occupied'),
        ('reserved',  'Reserved'),
    ]
    number   = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status   = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Table {self.number} ({self.status})"


# ─── 3. RESERVATIONS ────────────────────────────────────
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    table          = models.ForeignKey(Table, on_delete=models.CASCADE)  # allows multiple reservations for the same table (over time)  
    customer_name  = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    party_size     = models.IntegerField()
    date           = models.DateField()
    time           = models.TimeField()
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.customer_name} - Table {self.table.number} on {self.date}"


# ─── 4. ORDERS ──────────────────────────────────────────
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('preparing', 'Preparing'),
        ('served',    'Served'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    table       = models.ForeignKey(Table, on_delete=models.CASCADE)  # allows many orders per table
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def get_total(self) :

# Total calculation by summing subtotals of all order items:

        return sum(item.get_subtotal() for item in self.items.all())     # type: ignore

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number}"


class OrderItem(models.Model):
    
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name ='items') # many items per order
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity  = models.IntegerField(default=1)
    

    def get_subtotal(self):
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"


# ─── 5. INVENTORY ───────────────────────────────────────
class Inventory(models.Model):
    name            = models.CharField(max_length=100)
    quantity        = models.FloatField()
    unit            = models.CharField(max_length=20)  # e.g kg, litres, pieces
    low_stock_alert = models.FloatField(default=10)    # alert threshold

    def is_low(self):
        return self.quantity <= self.low_stock_alert

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


# ─── 6. PAYMENTS ────────────────────────────────────────
class Payment(models.Model):
    id = models.AutoField(primary_key=True)

    METHOD_CHOICES = [
        ('cash',   'Cash'),
        ('card',   'Card'),
        ('online', 'Online'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid',    'Paid'),
        ('failed',  'Failed'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # one payment per order
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} - {self.status}"