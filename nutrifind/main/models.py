import re
COLUMNS_LABELS = [
    'ndb_num',
    'name',
    'water',
    'calories',
    'protein',
    'total_fat',
    'ash',
    'total_carbs',
    'fiber', 
    'sugar_total', 
    'calcium',
    'iron',
    'magnesium',
    'phosphorous',
    'potassium',
    'sodium',
    'zinc',
    'copper',
    'manganese',
    'selenium',
    'vit_c',
    'thiamin',
    'riboflavin',
    'niacin',
    'panto_acid',
    'vit_b6',
    'folate_tot',
    'folic_acid',
    'food_folate',
    'folate_dfe',
    'choline_tot',
    'vit_b12',
    'vit_a',
    'vit_a_rae',
    'retinol',
    'alpha_carot',
    'beta_carot',
    'beta_crypt',
    'lycopene',
    'lutzea',
    'vit_e',
    'vit_d',
    'vit_d_iu',
    'vit_k',
    'sat_fat',
    'mono_fat',
    'poly_fat',
    'cholesterol',
]

from django.db import models
units = {
    'ounces':28.34,
    'ounce':28.34,
    'oz':28.34,
    'tbsp':14.3,
    'tbsps':14.3,
    'tsp':4.76666666667,
    'tsps':4.76666666667,
    'cup':8*28.34,
    'cups':8*28.34,
}

def fraction_to_float(amount_str):
    r = r'([0-9]+)\/([0-9]+)'
    match = re.match(r, amount_str)
    if match is None:
        return None

    groups = match.groups()
    num = groups[0]
    denom = groups[1]
    return float(num) / float(denom)

def fetch_ingredient(name):
    """
        Returns the nutrition facts about an ingredient with name `name`
        as a dictionary.
    """
    res = Ingredient.objects.filter(name__icontains=name).order_by('-preferred')
    if len(res) == 0:
        s = name.split(" ")
        s.reverse()

        res = Ingredient.objects.filter(name__icontains=",".join(s)).order_by('-preferred')
    return res

def get_data_from_string(string):
    """
        Returns the name and number of ounces of an ingredient given a string from a recipe.
        Returns None if no ingredient could be decoded.

        Example:

        '1 cup flour' => ('flour', )
    """

    amount_re = r'[\w\:\s]*([0-9]+[\/]?[0-9]*)\s([a-zA-Z\.]+)\s([a-zA-Z\.]+)'
    match = re.match(amount_re, string)

    if match is None:
        return None

    groups = match.groups()
    amount_str = groups[0]
    last_two = " ".join(groups[1:])
    if groups[1] in units:
        unit = groups[1]
        name_start_index = 1
    elif last_two in units:
        unit = last_two
        name_start_index = 2
    else:
        return None

    try:
        amount = float(amount_str)
    except ValueError:
        amount = fraction_to_float(amount_str)
        if amount is None:
            return None

    amount *= units[unit]
    name_re = r'[\w\:\s]*([0-9]+[\/]?[0-9]*)(\s([a-zA-Z\.]+))+'
    match = re.match(name_re, string)
    if match is None:
        return None
    groups = match.groups()

    words = groups[name_start_index:]

    s = ' '.join(words[:2])
    print amount, unit, words, s
    results = fetch_ingredient(s)
    if len(results) == 0:
        s = words[0]
    return s, amount




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

    preferred = models.BooleanField(default=False)

    @classmethod
    def from_json(cls, data):
        obj = cls(name=data['name'], calories=data['calories'], total_fat=data['fat'], total_carbs=data['carbs'])
        return obj

    def to_dict(self, ounces):
        result = {}
        for field in COLUMNS_LABELS:
            result[field] = getattr(self, field)
            if type(result[field]) is int:
                result[field] *= ounces
        return result

    def __unicode__(self):
        return self.name