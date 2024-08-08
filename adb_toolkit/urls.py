from django.urls import path
from .views import list_devices, device_detail, list_device_files, file_details
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('devices/', list_devices, name='list-devices'),
    path('devices/<str:device_id>/', device_detail, name='device-detail'),
    path('devices/<str:device_id>/files/', list_device_files, name='list-device-files'),
    path('devices/<str:device_id>/files/details/', file_details, name='file-details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
