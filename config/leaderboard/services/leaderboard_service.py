import leaderboard
from leaderboard.repositories.leaderboard_repository import LeaderboardRepository
from django.core.cache import cache

class LeaderboardService:

    @staticmethod
    def get_leaderboard(days=30,limit=10):
        raw_data = LeaderboardRepository.get_top_users_by_duration(
            days=days,
            limit=limit
        )

        leaderboard = []
        rank = 1

        for row in raw_data:
            leaderboard.append({
                'rank': rank,
                'user_id': row['user'],
                'total_duration': row['total_duration'],
            })
            rank += 1



        cache_key = 'leaderboard_30_days'
        cached = cache.get(cache_key)

        if cached:
            return cached

        cache.set(cache_key,leaderboard,timeout=600)

        return leaderboard