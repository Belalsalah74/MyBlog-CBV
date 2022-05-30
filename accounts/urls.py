from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView


app_name = 'accounts'
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/', LoginView.as_view(template_name='accounts/register.html',
         redirect_authenticated_user=True), name='login'),
    path('#', LogoutView.as_view(), name='logout'),
    path('logout/', views.LogoutConfirm.as_view(), name='logout-confirm'),
    path('profile/<int:pk>',views.ProfileDetail.as_view(),name='profile'),
    path('profile/<int:pk>/pass',
         PasswordChangeView.as_view(template_name='accounts/register.html', success_url='/'), name='password-change'),
    path('profile/<int:pk>/update/',views.ProfileUpdate.as_view(),name='profile-update'),
]   
