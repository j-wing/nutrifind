import sys, os, re
from main.models import Ingredient

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

def handle_line(line):
    # Exclude leading ~
    text_field_split = re.split('~([0-9a-zA-Z\,\s]+)~', line)

    columns = []
    columns.append(text_field_split[1])
    columns.append(text_field_split[3])

    # Eliminate leading empty string
    values = text_field_split[4].split("^")[1:]

    columns.extend(values)
    res = {}
    for i in range(len(COLUMNS_LABELS)):
        label = COLUMNS_LABELS[i]
        if type(label) is not str:
            index = label[0]
            name = label[1]
        else:
            name = label
            index = i

        if name == "name":
            split = name.split(",")
            res['general_name'] = split[0]
            res['desc'] = split[1:]

        res[name] = columns[index]
    return res



def main(filename):
    if not filename.startswith("/"):
        filename = os.path.join(os.path.dirname(__file__), filename)

    data = []
    with open(filename, 'r') as f:
        # i = 0
        for line in f:

            try:
                d = handle_line(line)
                ing = Ingredient(**d)
                ing.save()  
            except Exception as e:
                print "Encountered exception with:", d['name']
                print e
            # i+=1

if __name__ == '__main__':
    main(sys.argv[1])