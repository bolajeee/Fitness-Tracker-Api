from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class APISmokeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bolaji", password="StrongPass123!", email="b@example.com")
        # Login to get JWT
        url = reverse("token_obtain_pair")
        resp = self.client.post(url, {"username": "bolaji", "password": "StrongPass123!"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.access = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_create_activity_and_list(self):
        # Create
        resp = self.client.post("/api/activities/", {
            "type": "running",
            "date": "2025-08-24",
            "duration_minutes": 25,
            "calories_burned": 250,
            "distance_km": 4.5
        }, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # List my activities
        resp = self.client.get("/api/activities/?ordering=-date")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data["results"]), 1)  # paginated

    def test_history_endpoint_self(self):
        # create two activities
        for _ in range(2):
            self.client.post("/api/activities/", {
                "type": "cycling",
                "date": "2025-08-23",
                "duration_minutes": 60,
                "calories_burned": 500,
                "distance_km": 20
            }, format="json")

        # history
        url = f"/api/users/{self.user.id}/history/?order=-created_at"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data["results"]), 2)

    def test_permissions_users_me_only(self):
        # another user
        other = User.objects.create_user(username="other", password="StrongPass123!")
        # try to read other user's history (should 403)
        resp = self.client.get(f"/api/users/{other.id}/history/")
        self.assertEqual(resp.status_code, 403)
