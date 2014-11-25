import json, urllib2
from htmldom import htmldom

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from main.models import Ingredient, fetch_ingredient, get_data_from_string


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
    unable_to_find = []

    for i in range(nodes.len):
        node = nodes[i]
        text = node.text()

        data = get_data_from_string(text)
        if data is None:
            unable_to_find.append(text)
            continue

        name, amount = data
        ingredients = fetch_ingredient(name)
        if len(ingredients) == 0:
            unable_to_find.append(name)
            continue
        else:
            ingredient = ingredients.first()

        # d = {'name':name, 'grams':amount}
        # d.update(ingredient.to_dict(amount))
        # result.append(d)
        result.append("{0} -> {1}".format(text, name))


    return HttpResponse(json.dumps({'results':result, 'failures':unable_to_find}))