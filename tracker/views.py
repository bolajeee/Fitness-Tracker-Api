# views.py
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from django.views import View
from django.contrib.auth import login
from .models import CustomUser, Activity
from .serializers import UserSerializer, ActivitySerializer


def home_view(request):
    return render(request, 'base.html')  

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()  # Adding the queryset attribute

    # Limit non-admins to themselves
    def get_queryset(self):
        
        if self.request.user.is_staff:
            return super().get_queryset()
        return CustomUser.objects.filter(pk=self.request.user.pk)

    # Allow anyone to create an account
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    # Ensure users can only access their own data
    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)

        # only allow a user to delete themselves OR admin
        if request.user != user and not request.user.is_staff:
            return Response({"error": "You can only delete your own account."}, status=403)

        user.delete()
        return Response({"message": "User deleted successfully."}, status=204)

    @action(detail=True, methods=['get'], url_path='activities')
    def activities(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)

        activities = Activity.objects.filter(user=user)

        # query params: ?start_date=2025-01-01&end_date=2025-01-31
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        activity_type = request.query_params.get('type')

        if start_date:
            activities = activities.filter(date__gte=start_date)
        if end_date:
            activities = activities.filter(date__lte=end_date)
        if activity_type:
            activities = activities.filter(type=activity_type)

        activities = activities.order_by('-created_at')
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date", "duration_minutes", "calories_burned", "distance_km", "created_at"]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def metrics(self, request):
        activities = self.get_queryset()
        total_duration = activities.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        total_calories = activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        count = activities.count()

        return Response({
            "count": count,
            "total_duration": total_duration,
            "total_calories": total_calories,
            "avg_duration": total_duration / count if count > 0 else 0,
            "avg_calories": total_calories / count if count > 0 else 0,
        })
