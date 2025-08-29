# views.py
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from django.views import View
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from activities.models import Activity
from activities.serializers import ActivitySerializer


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
        # return self.queryset # all users 
        # if admin, return all users
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

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

