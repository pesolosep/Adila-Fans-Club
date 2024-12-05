from django.shortcuts import render
from search.query import *

# Create your views here.
def channel(request, channel_id):
    context = {}
    context["content"] = "channel.html"

    query_results = exec_query(QUERY_CHANNEL.replace('LABEL', channel_id))

    context["channel_id"] = channel_id
    context["channel_name"] = query_results[0]['name']['value']
    context["year_created"] = query_results[0]['yearCreated']['value']
    context["subscribers"] = query_results[0]['subscribers']['value']
    context["rank"] = query_results[0]['rank']['value']
    context["views_count"] = int(float(query_results[0]['videoViews']['value']))
    context["video_count"] = query_results[0]['videoCount']['value']
    context["category"] = unquote(query_results[0]['category']['value'])
    context["logo"] = query_results[0]['logo']['value'] if 'logo' in query_results[0] else None

    channel_videos = exec_query(QUERY_CHANNEL_VIDEOS.replace('LABEL', channel_id))
    context["channel_videos"] = channel_videos

    return render(request, 'base.html', context)


