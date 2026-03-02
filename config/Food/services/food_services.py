import requests
from django.conf import settings

from Food.cache import FoodCache


class FoodAPIService:
    BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"  #USDA search endpoint

    @staticmethod
    def search_food(query,page_size=5): # url parameters
        cached = FoodCache.get_search(query, page_size)
        if cached:
            return cached

        params = {
            'query': query,
            'page_size': page_size,
            'api_key': settings.USDA_API_KEY,
        }   #query=pizza&page_size=5&api_key=....

        response = requests.get(FoodAPIService.BASE_URL, params=params,timeout=10) # prevents the server from hanging forever
        response.raise_for_status() # automatically throws an error if anything goes wrong

        return response.json()