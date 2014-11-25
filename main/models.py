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
    'fluid ounces':28.34,
    'fl oz':28.34,
    'ounces':28.34,
    'ounce':28.34,
    'pound':453.592,
    'pounds':453.592,
    'clove':3.5,
    'cloves':3.5,
    'oz':28.34,
    'tbsp':14.3,
    'tbsps':14.3,
    'T':14.3,
    'tablespoon':14.3,
    'tablespoons':14.3,
    'tsp':4.76666666667,
    'tsps':4.76666666667,
    'teaspoon':4.76666666667,
    'teaspoons':4.76666666667,
    'cup':8*28.34,
    'cups':8*28.34,
    'pint':16*28.34,
    'pints':16*28.34,
    'quart':32*28.34,
    'quarts':32*28.34,
    'pinch':0.25
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
    print(name)
    res = Ingredient.objects.filter(name__icontains=name).order_by('-preferred')
    print(res)
    if len(res) == 0:
        s = name.split(" ")
        s.reverse()
        print "s:{0}\n\n".format(s)

        res = Ingredient.objects.filter(name__icontains=",".join(s)).order_by('-preferred')
    print "res:\n{0}\n".format(res)
    return res

def get_data_from_string(string):
    """
        Returns the name and number of ounces of an ingredient given a string from a recipe.
        Returns None if no ingredient could be decoded.

        Example:

        '1 cup flour' => ('flour', )
    """
    if string.split()[0] == "pinch":
        string = "1 " + string
    if string.find("OR") != -1:
        string = string[:string.find("OR")]
    print(string)
    # parse units first
    amount_re = r'[\w\:\s]*([0-9]+[\/]?[0-9]*)\s([a-zA-Z\.]+)\s([a-zA-Z\.]+)'
    match = re.match(amount_re, string)

    ### Need to fix recipe lines with "2-3" ingredients

    if match is None:

        print("aaaa!")
        return None

    groups = match.groups()
    amount_str = groups[0]
    last_two = " ".join(groups[1:]) #units can be two words (fl oz)
    if groups[1] in units:
        print("badsfad")
        unit = groups[1]
        name_start_index = 1
    elif last_two in units:
        unit = last_two
        name_start_index = 2
    else:
        print("SFDFSF")
        return None

    if unit not in units.keys():
        return None

    print("made it!")

    # parse number of units
    try:
        amount = float(amount_str)
    except ValueError:
        amount = fraction_to_float(amount_str)
        if amount is None:
            return None
    amount *= units[unit]

    # parse ingredient name
    # name_re = r'[\w\:\s]*([0-9]+[\/]?[0-9]*)(\s([a-zA-Z\.]+))+'
    # match = re.match(name_re, string)
    # if match is None:
    #     return None
    # groups = match.groups()
    # print "groups:{0}".format(groups)

    # words = groups[name_start_index:]

    string = get_rid_of_comments(string)

    words = string.split()[name_start_index+1:]

    s = ' '.join(words)
    print amount, unit, words, s
    results = fetch_ingredient(s)
    # if results fetch fails, then try to find match among individual words
    if len(results) == 0:
        # filter words first
        words = filter_words(words)
        print("words: {0}".format(words))
        total_results = []
        for word in words:
            results = fetch_ingredient(word)
            total_results += results
        best_result = get_best_result(total_results, words)[0]
        if best_result == None:
            s = ""
        else:
            s = best_result.name
    return s, amount

def get_rid_of_comments(string):
    """ COMMENTS (parantheticals) ARE STUPID """
    while string.find('(') != -1:
        start = string.find('(')
        end = string.find(')')
        if end != -1:
            string = string[:start] + string[end+1:]
    return string

def filter_words(words):
    filtered = []
    for word in words:
        if word[0] == "(":
            continue
        if word in ("and", "or", "of", "if", "plus", "optional", "choice"):
            continue
        if word in units.keys():
            continue
        if word.isdigit():
            continue
        if word == "sugar":
            filtered.append("granulated")
        if word == "chocolate":
            filtered.append("sweet")
        filtered.append(word)

    filtered = " ".join(filtered)
    comma_index = filtered.find(",")
    filtered = filtered
    if comma_index != -1:
        filtered = filtered[:comma_index]
    filtered = filtered.split()
    # filtered = filtered.split(",")
    # filtered = " ".join(filtered).split()
    return filtered

#filter "and" "or" and "of" from words

# filter results to choose one that contains most of the other words
# takes in list of results (ingredients) and all other words, and returns
# the result most likely fitting the recipe ingredient name
def get_best_result(results, words):
    print("/// Calling Best result ///")
    best_match = None
    most_matching_words = -1
    for result in results:
        matching_words = 0 #keep track of how many words are in result name

        words_in_result = filter_result_words(result)
        print(words_in_result, words)
        matches = []
        for word in words:
            # split words in ingredient name
            word = word.lower()
            if word in words_in_result:
                if word[len(word)-2:] == "ed":
                    matching_words += 1
                else:
                    matching_words += 2

                # elif len(words_in_result) > len(words):
                #     matching_words += 1

                matches.append(word)
        # print(matching_words, most_matching_words)
        if matching_words >= most_matching_words:
            print("## new best:{0}, {1}".format(result, matches))
            best_match = result
            most_matching_words = matching_words
    return best_match, most_matching_words

def filter_result_words(result):
    result_words = " ".join(result.name.lower().split(",")).split()
    filtered = []
    i = 0
    while i < len(result_words):
        word = result_words[i]
        if word == "no":
            word = "no " + result_words[i+1:i+2][0]
            i += 1
        if word == "pdr":
            word = "powder"
        if word == "sugars":
            word = "sugar"
        filtered.append(word)
        i += 1
    return filtered


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


