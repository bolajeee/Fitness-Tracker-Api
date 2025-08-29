from django.db import models
from django.conf import settings

# Create your models here.
class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activities")
    name = models.CharField(max_length=100)  # e.g., Running, Swimming
    duration_minutes = models.PositiveIntegerField()  # in minutes
    calories_burned = models.PositiveIntegerField()
    distance_km = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)  # gets set once when created
    updated_at = models.DateTimeField(auto_now=True)  # updates every save
    
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.user.email}"
