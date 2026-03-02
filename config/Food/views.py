from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from Food.services.food_services import FoodAPIService


class FoodAPIViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False)
    def search(self,request):
        query = request.query_params.get('q', '').strip()

        if not query:
            return Response(
                {'error': 'No search query provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = FoodAPIService.search_food(query)
        return Response(data)

