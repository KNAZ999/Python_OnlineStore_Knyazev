from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView  # ← добавлено

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='users/home.html'), name='home'),  # ← добавлено!
    path('users/', include('users.urls', namespace='users')),
    path('products/', include('Products.urls', namespace='Products')),
    path('cart/', include('Cart.urls', namespace='Cart')),
    path('accounts/', include('django.contrib.auth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)