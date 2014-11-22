from django.db import models

def fetch_nutrition_facts(name):
    """
        Returns the nutrition facts about an ingredient with name `name`
        as a dictionary.
    """
    return {'name':name, 'calories':28, 'fat':1, 'carbs':3}
def get_data_from_string(str):
    """
        Returns the name and number of ounces of an ingredient given a string from a recipe.
        Returns None if no ingredient could be decoded.

        Example:

        '1 cup flour' => ('flour', )
    """
    return "Pan Galactic Gargle Blaster", 17

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    total_fat = models.IntegerField()
    total_carbs = models.IntegerField()

    @classmethod
    def from_json(cls, data):
        obj = cls(name=data['name'], calories=data['calories'], total_fat=data['fat'], total_carbs=data['carbs'])
        return obj

    def to_dict(self, ounces):
        result = {}
        for field in ['name', 'calories', 'total_fat', 'total_carbs']:
            result[field] = getattr(self, field)
            if type(result[field]) is int:
                result[field] *= ounces
        return result