from django.contrib import admin
from django.urls import path, include
# WHY these two imports?
# path()    → creates a single URL pattern. Maps a URL string
#             to a view or another urls.py file.
# include() → lets us PLUG IN another urls.py file.
#             Instead of defining every URL in this one file,
#             we split them across apps and include them here.
#             This keeps code organized as the project grows.

urlpatterns = [
    path('admin/', admin.site.urls),
    # WHY is this already here?
    # Django put this here by default when we ran startproject.
    # It maps /admin/ to Django's built-in admin panel.
    # This is why http://127.0.0.1:8000/admin/ worked earlier!

    path('api/', include('core.urls')),
    # WHY 'api/' prefix?
    # This is a REST API convention — prefixing all API endpoints
    # with /api/ makes it clear these are API routes, not web pages.
    # So all our URLs now look like:
    #   /api/orders/
    #   /api/tables/
    #   /api/payments/
    #   etc.
    # include('core.urls') means "go find core/urls.py and
    # plug all its URL patterns in here under the /api/ prefix"
]