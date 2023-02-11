from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('register/', views.RegisterUserAPIView.as_view(), name="register_user"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/',views.get_movies, name="get_movies"),
    path('collection/',views.collections, name="collections"),
    path('collection/<uuid:uuid>/', views.collections, name="collection_by_id"),
    path('request-count/', views.get_requests_data, name="get_requests_data"),
    path('request-count/reset/', views.reset_requests_data, name="reset_requests_data")
]
