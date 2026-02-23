from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from leaderboard.services.leaderboard_service import LeaderboardService

class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        data = LeaderboardService().get_leaderboard()
        return Response(data)
    