from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum

# Template-based home page
def home_view(request):
    return render(request, 'templates/base.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# class ActivityViewSet(viewsets.ModelViewSet):
#     serializer_class = ActivitySerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['date', 'duration_minutes', 'calories_burned']
#
#     def get_queryset(self):
#         return Activity.objects.filter(user=self.request.user)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#     @action(detail=False, methods=['get'])
#     def summary(self, request):
#         activities = self.get_queryset()
#         total_duration = activities.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
#         total_distance = activities.aggregate(Sum('distance_km'))['distance_km__sum'] or 0
#         total_calories = activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
#         return Response({
#             "total_duration": total_duration,
#             "total_distance": total_distance,
#             "total_calories": total_calories
#         })
#
