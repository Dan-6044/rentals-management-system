from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('landlord/', views.landlord, name='landlord'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),  # Include user_id in URL
    path('add-property/<int:user_id>/', views.add_property, name='add-property'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
     path('update_property/<int:property_id>/', views.update_property, name='update_property'),
     path('delete_property/<int:property_id>/', views.delete_property, name='delete_property'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)