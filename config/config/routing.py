from django.urls import re_path
from workouts import consumers

websocket_urlpatterns = [
    re_path(r'was/workouts/$', consumers.WorkoutsConsumer.as_asgi()),
]

