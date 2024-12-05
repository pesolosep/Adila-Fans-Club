from django.http import JsonResponse
from fuzzywuzzy import fuzz
from django.shortcuts import render
from .query import *

def search(request):
    context = {}

    if request.method == 'POST':
        query = request.POST.get('query').strip()
        context["query"] = query

    context["content"] = "search.html"
    return render(request, 'base.html', context)

def autocomplete(request):
    assert request.method == 'POST'

    if request.method == 'POST':
        query = eval(request.body).get('query', '').strip()
        fuzzy_results = exec_query(FUZZY_QUERY.replace('LABEL', query))
        similars = []

        if len(fuzzy_results) < 1000:
            for data in fuzzy_results:
                ratio = fuzz.ratio(query.lower(), data['label']['value'].lower())
                similars.append((data, ratio))

            similars = sorted(similars, key=lambda x: x[1], reverse=True)
            similars = [x[0] for x in similars]
        else:
            similars = fuzzy_results

    return JsonResponse(similars, safe=False)