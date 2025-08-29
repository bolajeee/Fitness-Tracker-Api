from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from .serializers import ActivitySerializer
from .models import Activity


# Create your views here.
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date", "duration_minutes", "calories_burned", "distance_km", "created_at"]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='metrics')
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
