from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, ActivityViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"activities", ActivityViewSet, basename="activity")

urlpatterns = [
    path("api/", include(router.urls)),

    # JWT
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
