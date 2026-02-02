from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from workouts.models import Workout, Exercise
from django.contrib.auth.models import User
user = get_user_model()

class WorkoutAPItest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="testuser@example.com",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="otherpass123",
        )

        self.workout = Workout.objects.create(
            user=self.user,
            date='2024-01-01',
            duration='60',
            workout_type = 'STR'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_workout(self):
        """Test creating a new workout"""
        date = {
            'date': '2024-01-01',
            'duration': '60',
            'workout_type': 'STR',
            'notes':'Morning run'
        }
        response = self.client.post('/api/workouts/workouts/', data=date)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.username)
        self.assertEqual(Workout.objects.count(), 2)

    def test_user_cannot_see_others_workouts(self):
        """Test that the user cannot see others workouts"""

        Workout.objects.create(
            user=self.other_user,
            date='2024-01-02',
            duration='30',
            workout_type='HIIT'
        )
        response = self.client.get('/api/workouts/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),1)
        self.assertEqual(response.data['results'][0]['user'], self.user.username)

    def test_workout_stats_endpoint(self):
        """Test that the workout stats endpoint works correctly"""
        response = self.client.get('api/workouts/workouts/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_workouts', response.data)
        self.assertIn('toatl_duration', response.data)

    def test_today_workout_endpoint(self):
        """test todays workout endpoint"""
        response = self.client.get('/api/workouts/workouts/today')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

