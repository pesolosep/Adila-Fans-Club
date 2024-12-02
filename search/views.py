from SPARQLWrapper import SPARQLWrapper, JSON
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from django.shortcuts import render
from pprint import pprint as print

PREFIXES = """
    prefix :      <http://adilafanclub.com/base/>
    prefix owl:   <http://www.w3.org/2002/07/owl#>
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    prefix vcard: <http://www.w3.org/2006/vcard/ns#>
    prefix wd:    <http://www.wikidata.org/entity/>
    prefix xsd:   <http://www.w3.org/2001/XMLSchema#>
"""
OWL = "http://www.w3.org/2002/07/owl#"
HOST = "http://127.0.0.1:7200/"

sparql = SPARQLWrapper(f"{HOST}repositories/local_tk")


# Create your views here.
def search(request):
    response = {}

    if request.method == 'POST':
        query = request.POST.get('query').strip()
        sparql.setCredentials("admin", "root")
        sparql.setQuery(f"""
            {PREFIXES}

            SELECT ?id ?p ?o
            WHERE{{
                ?id rdfs:label :{query};
                    ?p ?o .
            }}
            """
        )

        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        response['data'] = results["results"]["bindings"]

    if not response["data"] and request.method == 'POST':
        sparql.setQuery(f"""
            {PREFIXES}

            SELECT ?id ?label
            WHERE{{
                ?id rdfs:label ?label;
            }}
            """
        )
        fuzzy_results = sparql.query().convert()
        fuzzy_data = fuzzy_results["results"]["bindings"]
        similar_ids = []

        for data in fuzzy_data:
            ratio = fuzz.ratio(query, data['label']['value'].removeprefix(OWL))

            if ratio >= 50:
                similar_ids.append(data['id']['value'])

    context = {}
    context["content"] = "search.html"
    return render(request, 'base.html', context)
