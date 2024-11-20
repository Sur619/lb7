from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from MySite import views
from MySite.views import vote

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('MySite.urls')),
    path('auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.home, name='home'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/profile/', views.profile, name='profile'),
    path('api/edit_profile/', views.edit_profile, name='edit_profile'),
    path('vote/<int:category_id>/', vote, name='vote'),
    path('api/profile/history/', views.history, name='history'),

]
