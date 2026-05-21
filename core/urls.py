# Routing requests to the appropriate viewsets based on URL patterns.(The right view)

from rest_framework.routers import DefaultRouter
# WHY DefaultRouter?
# A router is a special Django REST Framework tool that
# AUTOMATICALLY generates all the URLs for our viewsets.
# Without it we'd have to manually write a URL pattern for every
# single action (list, create, retrieve, update, delete) — that's
# 5 URLs per viewset × 6 viewsets = 30 URL patterns manually.
# DefaultRouter generates all of them with just ONE line per viewset.

from .views import (CategoryViewSet, MenuItemViewSet, TableViewSet,
                    ReservationViewSet, OrderViewSet, InventoryViewSet,
                    PaymentViewSet)
# WHY import views here?
# The router needs to know WHICH viewset handles WHICH URL.
# So we import all our viewsets and register them below.

router = DefaultRouter()
# WHY create a router instance?
# This creates the actual router object we'll register our
# viewsets on. Think of it as creating the reception desk
# before you can assign staff to it.

router.register(r'categories', CategoryViewSet)
# WHY r'categories'?
# This is the URL PREFIX for this viewset.
# The r'' means raw string — backslashes are treated literally.
# After registering, Django auto-generates these URLs:
#   GET    /categories/         → list all categories
#   POST   /categories/         → create a category
#   GET    /categories/{id}/    → get one category
#   PUT    /categories/{id}/    → update a category
#   DELETE /categories/{id}/    → delete a category
#   GET    /categories/         → custom actions we defined

router.register(r'menu', MenuItemViewSet)
# Same pattern — all CRUD endpoints now exist at /menu/
# Plus our custom: GET /menu/available/

router.register(r'tables', TableViewSet)
# All CRUD at /tables/
# Plus our custom: GET /tables/available/

router.register(r'reservations', ReservationViewSet)
# All CRUD at /reservations/
# Our overridden create() runs when POST /reservations/ is called

router.register(r'orders', OrderViewSet)
# All CRUD at /orders/
# Plus our custom: PATCH /orders/{id}/update_status/

router.register(r'inventory', InventoryViewSet)
# All CRUD at /inventory/
# Plus our custom: GET /inventory/low_stock/

router.register(r'payments', PaymentViewSet)
# All CRUD at /payments/
# Our overridden create() runs when POST /payments/ is called

urlpatterns = router.urls
# WHY router.urls?
# This extracts ALL the generated URL patterns from the router
# into a list called urlpatterns.
# Django specifically looks for a variable named urlpatterns
# in urls.py — it MUST be named exactly this.
# router.urls contains every URL we registered above, fully built.