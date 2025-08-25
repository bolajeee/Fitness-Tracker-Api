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

    @action(detail=True, methods=["get"], url_path="activity")
    def history(self, request, pk=None):
        # Admin can view anyone; normal users only themselves
        user = get_object_or_404(CustomUser, pk=pk)
        if not (request.user.is_staff or request.user.pk == user.pk):
            return Response({"detail": "Forbidden"}, status=403)

        qs = Activity.objects.filter(user=user)

        # Optional sorting via ?order=-created_at
        order = request.query_params.get("order", "-created_at")
        allowed = {"created_at", "-created_at", "date", "-date", "duration_minutes",
                   "-duration_minutes", "calories_burned", "-calories_burned"}
        if order not in allowed:
            order = "-created_at"

        activities = qs.order_by(order)
        page = self.paginate_queryset(activities)
        ser = ActivitySerializer(page or activities, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date", "duration_minutes", "calories_burned", "distance_km", "created_at"]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        agg = qs.aggregate(
            total_duration=Sum("duration_minutes"),
            total_calories=Sum("calories_burned"),
            total_distance=Sum("distance_km"),
        )
        # Replace None with 0
        for k in agg:
            agg[k] = agg[k] or 0
        return Response(agg)
