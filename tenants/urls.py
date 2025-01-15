from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('tenant/', views.tenant, name='tenant'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('ten_dashboard/<int:user_id>/', views.ten_dashboard, name='ten_dashboard'),  # Include user_id in URL
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

