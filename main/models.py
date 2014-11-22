import re

from django.db import models
units = [
    'fluid'
    'ounces',
    'ounce',
    'oz',
    'tbsp',
    'tbsps',
    'tsp',
    'tsps',
    'cup',
    'cups',
]

def fetch_nutrition_facts(name):
    """
        Returns the nutrition facts about an ingredient with name `name`
        as a dictionary.
    """
    return {'name':name, 'calories':28, 'fat':1, 'carbs':3}

def get_data_from_string(string):
    """
        Returns the name and number of ounces of an ingredient given a string from a recipe.
        Returns None if no ingredient could be decoded.

        Example:

        '1 cup flour' => ('flour', )
    """

    amount_re = r'[\w\:\s]*([0-9]+[\/]?[0-9]*)\s([a-zA-Z\.]+)\s([a-zA-Z\.]+)\s'
    match = re.match(amount_re, string)
    if match is None:
        return None

    groups = match.groups()
    amount = groups[0]
    last_two = " ".join(groups[1:])
    if groups[1] in units:
        unit = groups[1]
    elif last_two in units:
        unit = last_two
    else:
        return None

    return "Pan Galactic Gargle Blaster", 17

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    general_name = models.CharField(max_length=255, null=True)
    desc = models.CharField(max_length=255, null=True)
    ndb_num = models.IntegerField(default=0)
    water = models.FloatField(default=0.0)
    calories = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0)
    total_fat = models.FloatField(default=0.0)
    ash = models.FloatField(default=0.0)
    total_carbs = models.FloatField(default=0.0)
    fiber = models.FloatField(default=0.0)
    sugar_total = models.FloatField(default=0.0)
    calcium = models.FloatField(default=0.0)
    iron = models.FloatField(default=0.0)
    magnesium = models.FloatField(default=0.0)
    phosphorous = models.FloatField(default=0.0)
    potassium = models.FloatField(default=0.0)
    sodium = models.FloatField(default=0.0)
    zinc = models.FloatField(default=0.0)
    copper = models.FloatField(default=0.0)
    manganese = models.FloatField(default=0.0)
    selenium = models.FloatField(default=0.0)
    vit_c = models.FloatField(default=0.0)
    thiamin = models.FloatField(default=0.0)
    riboflavin = models.FloatField(default=0.0)
    niacin = models.FloatField(default=0.0)
    panto_acid = models.FloatField(default=0.0)
    vit_b6 = models.FloatField(default=0.0)
    folate_tot = models.FloatField(default=0.0)
    folic_acid = models.FloatField(default=0.0)
    food_folate = models.FloatField(default=0.0)
    folate_dfe = models.FloatField(default=0.0)
    choline_tot = models.FloatField(default=0.0)
    vit_b12 = models.FloatField(default=0.0)
    vit_a = models.FloatField(default=0.0)
    vit_a_rae = models.FloatField(default=0.0)
    retinol = models.FloatField(default=0.0)
    alpha_carot = models.FloatField(default=0.0)
    beta_carot = models.FloatField(default=0.0)
    beta_crypt = models.FloatField(default=0.0)
    lycopene = models.FloatField(default=0.0)
    lutzea = models.FloatField(default=0.0)
    vit_e = models.FloatField(default=0.0)
    vit_d = models.FloatField(default=0.0)
    vit_d_iu = models.FloatField(default=0.0)
    vit_k = models.FloatField(default=0.0)
    sat_fat = models.FloatField(default=0.0)
    mono_fat = models.FloatField(default=0.0)
    poly_fat = models.FloatField(default=0.0)
    cholesterol = models.FloatField(default=0.0)

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

    def __unicode__(self):
        return self.name