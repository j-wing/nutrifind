import json, urllib2
from htmldom import htmldom

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")

def names(request):
    d = [{'name':'Bob'}, {'name':'Joe'}]
    return HttpResponse(json.dumps(d))

def get_ingredients(request):
    url = request.GET.get("url")
    contents = urllib2.urlopen(url).read()
    print "done yp"
    dom = htmldom.HtmlDom().createDom(contents)
    nodes = dom.find("[itemprop=ingredients]")
    print "nodes"

    result = [nodes[i].text() for i in range(nodes.len)]
    return HttpResponse(json.dumps(result))