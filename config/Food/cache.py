from django.core.cache import cache

class FoodCache:

    @staticmethod
    def get_search(query):
        return cache.get(f'food_search:{query.lower()}') # to prevent duplicate caching for the same word but cases

    @staticmethod
    def set_search(query,data,timeout=86400): # 24hrs in seconds
        cache.set(
            f'food_search:{query.lower()}',
            data,
            timeout
        ) # stores each value passed into redis