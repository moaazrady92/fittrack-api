class FoodParser:

    @staticmethod
    def parse_usda_food(food):
        nutrients = food.get('foodNutrients', []) #means return the value if exists else return an empty list

        def get_nutrient(name):
            for n in nutrients:
                if n.get('nutrientName','').lower() == name.lower(): #safe extraction, .lower for case-insensitive comparison
                    return n.get('value', 0) # return value of n if missing return zero (for example if the product doesn't have protein it returns zero)

            return 0

        return {
            'name': food.get('description'),  # .get('') its defined in their site
            'brand' : food.get('brandOwner'),
            'calories' : get_nutrient('Energy'),
            'protein' : get_nutrient('Protein'),
            'carbs': get_nutrient('Carbohydrate, by difference'),
            'fats' : get_nutrient('total lipid (fat)'),
        }
