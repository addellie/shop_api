from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('authorisation/', views.AuthorizationAPIView.as_view()),
    path('comfirm', views.confirm_api_view),
]
