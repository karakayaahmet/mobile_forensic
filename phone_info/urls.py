from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('search', views.search, name='search'),
                  path('create-phone', views.create_phone, name='create_phone'),
                  path('phone_info', views.phone_info_view, name='phone_info'),
                  path('phone-list', views.phone_list, name='phone_list'),
                  path('phone-edit/<int:id>', views.phone_edit, name='phone_edit'),
                  path('phone-delete/<int:id>', views.phone_delete, name='phone_delete'),
                  path('<slug:slug>', views.details, name='phone_details'),
                  path('category/<slug:slug>', views.get_phone_by_category, name='phone_by_category')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)