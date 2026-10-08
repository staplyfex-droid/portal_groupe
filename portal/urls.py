from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="portal/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path('diary', views.DiaryView.as_view(), name='diary'),
    path('edit-grade/<int:pk>/', views.GradeUpdateView.as_view(), name='edit_grade'),
    path('delete-grade/<int:pk>/', views.GradeDeleteView.as_view(), name='delete_grade')
]