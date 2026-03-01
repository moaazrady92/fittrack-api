from leaderboard.repositories.leaderboard_repository import LeaderboardRepository
from django.core.cache import cache

class LeaderboardService:

    @staticmethod
    def get_leaderboard(days=30,limit=10):
        cache_key = f'leaderboard_{days}_days_{limit}'

        cached = cache.get(cache_key)
        if cached:
            return cached

        raw_data = LeaderboardRepository.get_top_users_by_duration(
            days=days,
            limit=limit
        )
        leaderboard = []

        for rank,row in enumerate(raw_data,start=1):
            leaderboard.append({
                'rank': rank,
                'user_id': row['user'],
                'total_duration': row['total_duration'],
            })
        cache.set(cache_key,leaderboard,timeout=600) #storing data in the memory for 10minutes

        return leaderboard

