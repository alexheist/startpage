from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("switch-read/", views.switch_read),
    path("switch-write/", views.switch_write),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
