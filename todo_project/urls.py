# todo_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from todo_app import views as todo_views

urlpatterns = [
    # Page d'accueil principale
    path('', todo_views.index, name='home'),

    # URLs d'authentification
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/signup/', todo_views.signup, name='signup'),
    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),
    path('accounts/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
path('car-prediction/', include('car_prediction.urls')),

    # URLs de l'application TODO
    path('todo/', include('todo_app.urls')),

    # NEW: URLs for Car Prediction App
    path('car-prediction/', include('car_prediction.urls')),

    # Admin
    path('admin/', admin.site.urls),

    # Django Browser Reload
    path("__reload__/", include("django_browser_reload.urls")),
]