import json
from channels.generic .websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Workout

User = get_user_model()

class WorkoutsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name =f'workouts_{self.user.id}'

        if self.user.is_anonymous:
            await self.close()

        else:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': 'Websocket connected for workout updates'
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        if message_type == 'subscribe_workout':
            workout_id = text_data_json['workout_id']
            await self.subscribe_to_workout(workout_id)

    @database_sync_to_async
    def subscribe_to_workout(self, workout_id):
        try:
            workout = Workout.objects.get(pk=workout_id,user=self.user)
            return True
        except Workout.DoesNotExist:
            return False


    async def workout_update(self,event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'type': 'workout_update',
            'message': message
        }))