import json, urllib2
from htmldom import htmldom

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from main.models import Ingredient, fetch_nutrition_facts, get_data_from_string


def index(request):
    return render(request, "index.html")

def names(request):
    d = [{'name':'Bob'}, {'name':'Joe'}]
    return HttpResponse(json.dumps(d))

def get_ingredients(request):
    url = request.GET.get("url")
    contents = urllib2.urlopen(url).read()
    dom = htmldom.HtmlDom().createDom(contents)
    nodes = dom.find("[itemprop=ingredients]")

    if nodes.len > 25:
        return HttpResponse("Error: too many ingredients! (%s)" % nodes.len)

    result = []

    for i in range(nodes.len):
        node = nodes[i]
        text = node.text()

        name, ounces = get_data_from_string(text)
        ingredients = Ingredient.objects.filter(name=name)
        if len(ingredients) == 0:
            data = fetch_nutrition_facts(name)
            ingredient = Ingredient.from_json(data)
            ingredient.save()
        else:
            ingredient = ingredients.first()

        d = {'name':name, 'ounces':ounces}
        d.update(ingredient.to_dict(ounces))
        result.append(d)


    return HttpResponse(json.dumps(result))