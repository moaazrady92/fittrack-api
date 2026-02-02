from rest_framework import status


def test_workout_duration_validation(self):
    data = {
        'date': '2024-01-15',
        'duration': 0,
        'workout_type': 'STR',
    }
    response = self.client.post('api/workouts/workouts/',data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('duration', response.data)