from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('flisting', views.food_listings, name='food_listing'),
    path('listing/<int:listing_id>/', views.food_detail, name='food_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', LoginView.as_view(template_name='donation/login.html'), name='login'),
    path('ngo/login/', views.ngo_login, name='ngo_login'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/ngo/', views.register_ngo, name='register_ngo'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('ngo/dashboard/', views.ngo_dashboard, name='ngo_dashboard'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('request/<int:listing_id>/', views.request_food, name='request_food'),
    path('manage-request/<int:request_id>/<str:action>/', views.manage_request, name='manage_request'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


