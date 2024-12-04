from SPARQLWrapper import SPARQLWrapper, JSON
from django.http import JsonResponse
from fuzzywuzzy import fuzz
from django.shortcuts import render
from .query import *
from django.conf import settings

sparql = SPARQLWrapper(REPO)

def search(request):
    context = {}

    if request.method == 'POST':
        query = request.POST.get('query').strip()
        fuzzy_results = exec_query(FUZZY_QUERY)
        prefixed = []
        infixed = []
        similars = []

        for data in fuzzy_results:
            cond = data['label']['value'].lower().startswith(query.lower())
            if cond:
                prefixed.append(data)

            cond2 = query.lower() in data['label']['value'].lower()
            if not cond and cond2:
                infixed.append(data)

            ratio = fuzz.ratio(query.lower(), data['label']['value'].lower())
            if not cond and not cond2 and ratio >= 80:
                similars.append((data, ratio))

            similars = sorted(similars, key=lambda x: x[1], reverse=True)

        similars = [x[0] for x in similars]
        context["data"] = prefixed + infixed + similars

    context["content"] = "search.html"

    return render(request, 'base.html', context)

def exec_query(query: str) -> dict:
    sparql.setCredentials(settings.DB_UNAME, settings.DB_PASS)
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results["results"]["bindings"]

def autocomplete(request):
    assert request.method == 'POST'

    if request.method == 'POST':
        query = eval(request.body).get('query', '').strip()
        fuzzy_results = exec_query(FUZZY_QUERY)
        prefixed = []
        infixed = []
        similars = []

        for data in fuzzy_results:
            data['id']['value'] = data['id']['value'].removeprefix(BASE)
            cond = data['label']['value'].lower().startswith(query.lower())
            if cond:
                prefixed.append(data)

            cond2 = query.lower() in data['label']['value'].lower()
            if not cond and cond2:
                infixed.append(data)

            ratio = fuzz.ratio(query.lower(), data['label']['value'].lower())
            if not cond and not cond2 and ratio >= 80:
                similars.append((data, ratio))

            similars = sorted(similars, key=lambda x: x[1], reverse=True)

        similars = [x[0] for x in similars]

    return JsonResponse((prefixed + infixed + similars)[:50], safe=False)
