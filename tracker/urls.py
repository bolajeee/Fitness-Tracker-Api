from rest_framework.routers import DefaultRouter
from .views import UserViewSet, home_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('/api', home_view, name='home'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
