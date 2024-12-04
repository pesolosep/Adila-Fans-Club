from multiprocessing import context
import SPARQLWrapper
from django.shortcuts import render
from search.query import *
from search.views import exec_query

# Create your views here.
def channel(request, channel_id):
    context = {}
    query_results = exec_query(QUERY_CHANNEL.replace('LABEL', channel_id))
    print(query_results)

    context["content"] = "channel.html"
    context["channel_name"] = query_results[0]['name']['value']
    context["year_created"] = query_results[0]['yearCreated']['value']
    context["subscribers"] = query_results[0]['subscribers']['value']
    context["rank"] = query_results[0]['rank']['value']
    context["video_views"] = query_results[0]['videoViews']['value']
    context["video_count"] = query_results[0]['videoCount']['value']
    context["category"] = query_results[0]['category']['value']

    return render(request, 'base.html', context)


