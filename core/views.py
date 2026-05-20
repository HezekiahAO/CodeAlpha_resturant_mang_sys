from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, MenuItem, Table, Reservation, Order, OrderItem, Inventory, Payment
from .serializers import (CategorySerializer, MenuItemSerializer, TableSerializer,
                          ReservationSerializer, OrderSerializer, OrderItemSerializer,
                          InventorySerializer, PaymentSerializer)


# ─── A bit of explanation for better understanding ────────────────────────────────────────────────
# timezone     → Django's way of handling time. Always use this instead of
#                Python's built-in datetime because it respects your timezone
#                settings in settings.py

# viewsets     → A viewset is a class that handles multiple related API actions
#                (list all, create one, get one, update, delete) in ONE place.
#                Without viewsets you'd write a separate function for each action.

# status       → This gives us readable HTTP status codes like:
#                status.HTTP_200_OK (success)
#                status.HTTP_201_CREATED (something was created)
#                status.HTTP_400_BAD_REQUEST (client sent bad data)
#                Instead of remembering raw numbers like 200, 201, 400

# action       → A decorator that lets us add CUSTOM endpoints to a viewset
#                beyond the default CRUD ones. For example /tables/available/

# Response     → Django REST Framework's way of sending data back to the client.
#                It automatically converts Python dicts/objects to JSON



# ════════════════════════════════════════════════════════════════════════════
# ─── MENU VIEWS ─────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════

class CategoryViewSet(viewsets.ModelViewSet):
    # WHY ModelViewSet?
    # ModelViewSet is a pre-built class from Django REST Framework that
    # automatically gives us these 5 endpoints for FREE, this are :
    #   GET    /categories/        → list all categories
    #   POST   /categories/        → create a new category
    #   GET    /categories/{id}/   → get one category
    #   PUT    /categories/{id}/   → update a category
    #   DELETE /categories/{id}/   → delete a category
    # We don't have to write any of that logic ourselves!

    queryset = Category.objects.all()
    # Queryset?
    # This tells Django WHICH data to work with.
    # Category.objects.all() means "fetch all rows from the Category table"
    # Think of it like SELECT * FROM category in SQL

    serializer_class = CategorySerializer
    # Serializer_class?
    # This tells the viewset WHICH serializer to use when converting
    # data to/from JSON. Serializers are translators from JSON to Pyhton and vise versa.


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    @action(detail=False, methods=['get'])
    # @action?
    # This decorator creates a CUSTOM endpoint outside the default CRUD ones.
    # detail=False means this action works on the WHOLE collection, not one item
    #   → URL will be: /menu/available/
    # detail=True would mean it works on ONE specific item
    #   → URL would be: /menu/{id}/available/
    # methods=['get'] means only GET requests are allowed here

    def available(self, request):
        # WHY filter(is_available=True)?
        # Instead of fetching ALL menu items and filtering in Python,
        # we let the DATABASE do the filtering — it's much faster.
        # This is like SQL: SELECT * FROM menuitem WHERE is_available = true
        available_items = MenuItem.objects.filter(is_available=True)

        # WHY get_serializer?
        # self.get_serializer() is a helper method from ModelViewSet.
        # many=True tells it we're serializing a LIST of items, not just one.
        # Without many=True it would expect a single object and crash.
        serializer = self.get_serializer(available_items, many=True)

        return Response(serializer.data)
        # WHY serializer.data?
        # After serializing, the JSON-ready data lives in serializer.data
        # Response() wraps it and sends it back to whoever made the request



# ════════════════════════════════════════════════════════════════════════════
# ─── TABLE VIEWS ────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        # WHY filter here instead of in the serializer?
        # Filtering belongs in the VIEW (business logic layer), not the
        # serializer (translation layer). Each layer should do ONE job.
        # View = decides WHAT data to return
        # Serializer = decides HOW to format that data
        available_tables = Table.objects.filter(status='available')
        serializer = self.get_serializer(available_tables, many=True)
        return Response(serializer.data)



# ════════════════════════════════════════════════════════════════════════════
# ─── RESERVATION VIEWS ──────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        # WHY override create()?
        # The DEFAULT create() from ModelViewSet just saves data to the DB.
        # But making a reservation has EXTRA logic:
        #   1. Check if the table is actually available
        #   2. If yes → save the reservation
        #   3. Also update the table status to 'reserved'
        # The default create() doesn't know about any of that.
        # So we override it and add our custom logic.

        # WHY *args, **kwargs?
        # These capture any extra arguments passed to the function.
        # Django's routing system sometimes passes extra data and
        # we need to accept it even if we don't use it directly.

        serializer = self.get_serializer(data=request.data)
        # WHY data=request.data?
        # request.data contains the JSON body sent by the client.
        # We pass it to the serializer so it can validate and
        # convert it into Python objects we can work with.

        serializer.is_valid(raise_exception=True)
        # WHY is_valid()?
        # This runs all validation rules defined in the serializer.
        # For example: is the date format correct? Does the table exist?
        # raise_exception=True means if validation FAILS, automatically
        # return a 400 error with details — we don't handle it manually.

        table = serializer.validated_data['table']
        # WHY validated_data instead of request.data?
        # request.data is raw JSON (strings, numbers from the client)
        # validated_data is CLEAN Python objects after validation.
        # For example, 'table' in request.data is just an ID number (3)
        # but in validated_data it's an actual Table object we can use.

        if table.status != 'available':
            # WHY this check?
            # This is pure BUSINESS LOGIC. A restaurant can't reserve
            # a table that's already occupied or reserved.
            # We check BEFORE saving so we never create bad data in the DB.
            return Response(
                {'error': f'Table {table.number} is not available'},
                status=status.HTTP_400_BAD_REQUEST
                # WHY 400? HTTP 400 = "Bad Request" — the client sent a
                # request that can't be fulfilled due to a business rule.
            )

        reservation = serializer.save()
        # WHY serializer.save()?
        # This actually writes the reservation to the database.
        # We only reach this line if the table IS available — good.

        table.status = 'reserved'
        table.save()
        # WHY two separate saves?
        # Reservation and Table are two different database tables (models).
        # Saving the reservation doesn't automatically update the table.
        # We have to explicitly update and save the table ourselves.
        # This is the CORE connection logic between two domains.

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # WHY 201 and not 200?
        # HTTP 200 = "OK, here's data you asked for" (usually GET requests)
        # HTTP 201 = "Something new was CREATED successfully"
        # Using the right status code tells the client exactly what happened.



# ════════════════════════════════════════════════════════════════════════════
# ─── ORDER VIEWS ────────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # WHY is this the most complex view?
        # Placing an order touches THREE models at once:
        #   1. Order       → create the order record
        #   2. OrderItem   → create one record per item ordered
        #   3. Table       → update its status to 'occupied'
        # This is the heart of the whole system.

        table_id = request.data.get('table')
        items_data = request.data.get('items', [])
        # WHY .get('items', [])?
        # .get() is safer than request.data['items'] because if 'items'
        # key doesn't exist in the request, .get() returns the default
        # value [] instead of crashing with a KeyError.

        if not items_data:
            # WHY validate early?
            # "Fail fast" principle — catch problems as early as possible
            # before doing any database operations. No point creating an
            # Order record if there are no items to put in it.
            return Response(
                {'error': 'Order must have at least one item'},
                status=status.HTTP_400_BAD_REQUEST
            )

        table = Table.objects.get(id=table_id)
        # WHY Table.objects.get() and not filter()?
        # .get() returns EXACTLY ONE object or raises an error.
        # .filter() returns a queryset (list) even if only one item matches.
        # Since table IDs are unique, we KNOW we want exactly one — use .get()

        order = Order.objects.create(table=table)
        # WHY create the Order before the OrderItems?
        # OrderItem has a ForeignKey to Order — it NEEDS the order to exist
        # first before it can be linked to it. This is the required sequence.

        for item_data in items_data:
            # WHY a loop?
            # A customer can order multiple different items.
            # Each item in the request becomes its own OrderItem row in the DB.
            # Example request items: [
            #   {"menu_item": 1, "quantity": 2},  → 2x Burger
            #   {"menu_item": 3, "quantity": 1}   → 1x Juice
            # ]
            menu_item = MenuItem.objects.get(id=item_data['menu_item'])
            quantity = item_data.get('quantity', 1)
            # WHY default quantity of 1?
            # If the client doesn't specify quantity, we assume they want 1.
            # Better than crashing or creating a quantity-0 order item.

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity
            )

        table.status = 'occupied'
        table.save()
        # WHY mark as occupied here?
        # Once a real order is placed (not just a reservation),
        # the table is ACTIVELY being used. This prevents other
        # orders or reservations from being assigned to it.

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    # WHY detail=True here but detail=False earlier?
    # detail=True = this action targets ONE specific order
    # URL will be: /orders/{id}/update_status/
    # We need the ID because we're updating a SPECIFIC order's status.
    # methods=['patch'] because PATCH = partial update (just the status field)
    # We're not replacing the whole order, just changing one field.

    def update_status(self, request, pk=None):
        # WHY pk=None?
        # pk = primary key = the ID in the URL (/orders/5/update_status/)
        # Django passes it here automatically. We default it to None
        # as a safety measure in case it's somehow not provided.

        order = self.get_object()
        # WHY get_object() instead of Order.objects.get(id=pk)?
        # get_object() is a ModelViewSet helper that:
        #   1. Fetches the object by pk automatically
        #   2. Returns a 404 automatically if not found
        # It saves us from writing that logic ourselves.

        new_status = request.data.get('status')

        VALID_STATUSES = ['pending', 'preparing', 'served', 'completed', 'cancelled']
        if new_status not in VALID_STATUSES:
            # WHY validate the status value?
            # We can't let someone set order status to "banana" or anything
            # random. We enforce only the values our system understands.
            return Response(
                {'error': f'Invalid status. Choose from {VALID_STATUSES}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()

        if new_status in ['completed', 'cancelled']:
            order.table.status = 'available'
            order.table.save()
            # WHY auto-free the table?
            # When an order is done or cancelled, that table is no longer
            # in use. We automatically release it so it can be assigned
            # to new customers. This is the system "closing the loop"
            # on the restaurant session that started with a reservation.



# ════════════════════════════════════════════════════════════════════════════
# ─── INVENTORY VIEWS ────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        # WHY a list comprehension here instead of .filter()?
        # is_low() is a Python METHOD on the model, not a database column.
        # The database doesn't know about is_low() — it only knows about
        # actual columns like quantity and low_stock_alert.
        # So we have to fetch all items first, then filter in Python.
        # The trade-off: slightly less efficient than a DB query but
        # it keeps the low-stock logic in ONE place (the model).
        low_items = [item for item in Inventory.objects.all() if item.is_low()]
        serializer = self.get_serializer(low_items, many=True)
        return Response(serializer.data)



# ════════════════════════════════════════════════════════════════════════════
# ─── PAYMENT VIEWS ──────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════════════

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # WHY override create() for payments?
        # Default create() would require the client to manually send the amount.
        # That's dangerous — what stops them from sending amount=0?
        # Instead we CALCULATE the amount from the order total ourselves.
        # The client only needs to send: order ID and payment method.

        order_id = request.data.get('order')
        method = request.data.get('method')

        order = Order.objects.get(id=order_id)

        if hasattr(order, 'payment') and order.payment.status == 'paid':  # type: ignore
            # WHY hasattr()?
            # hasattr() checks if the order object HAS a 'payment' attribute.
            # Because Payment has a OneToOneField to Order, Django creates
            # a reverse 'payment' attribute on Order automatically.
            # But if no payment exists yet, accessing order.payment would CRASH.
            # hasattr() safely checks first before we try to access it.
            return Response(
                {'error': 'This order has already been paid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = Payment.objects.create(
            order=order,
            amount=order.get_total(),
            # WHY get_total() here?
            # This calculates the bill by summing all OrderItem subtotals.
            # The amount is DERIVED from the order — not entered manually.
            # This ensures the payment always matches what was actually ordered.
            method=method,
            status='paid',
            paid_at=timezone.now()
            # WHY timezone.now() and not datetime.now()?
            # timezone.now() respects the timezone settings in settings.py
            # datetime.now() always uses the server's local time which could
            # be wrong if your server is in a different timezone than your
            # restaurant. Always use Django's timezone utility for time.
        )

        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)