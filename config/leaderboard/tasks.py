from celery import shared_task
from .services.leaderboard_service import LeaderboardService

@shared_task
def rebuild_leaderboard():
    LeaderboardService.get_leaderboard(days=30,limit=10)