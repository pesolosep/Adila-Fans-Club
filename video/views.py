from django.shortcuts import render
from search.query import *
from datetime import datetime


# Create your views here.
def video(request, video_id):
    context = {}

    video_data = exec_query(QUERY_VIDEO.replace("LABEL", video_id))
    data_date = {}
    data_date_country = {}

    for video in video_data:
        date = {
            "weeklyMovement": video["weeklyMovement"]["value"],
            "dailyMovement": video["dailyMovement"]["value"],
            "dailyRank": video["dailyRank"]["value"],
            "datePublished": datetime.strptime(video["datePublished"]["value"], '%Y-%m-%d %H:%M:%S%z').date(),
            "viewCount": video["viewCount"]["value"],
            "likeCount": video["likeCount"]["value"],
            "commentCount": video["commentCount"]["value"],
            "title": video["title"]["value"],
            "desc": video["desc"]["value"],
            "language": video["language"]["value"],
            "thumb": video["thumb"]["value"],
            "tags": video["tags"]["value"].split(", ") if "tags" in video else []
        }

        data_date[video["collectedDate"]["value"]] = []
        data_date_country[(video["collectedDate"]["value"], video["country"]["value"])] = date

    for video in video_data:
        data_date[video["collectedDate"]["value"]].append(video["country"]["value"])

    context["content"] = "video.html"
    data_date = [(k, v) for k, v in data_date.items()]


    if request.method == "POST":
        context['date'] = request.POST.get("date_select")
    else:
        context['date'] = data_date[0][0]

    data_date = {k: v for k, v in data_date}

    context['countries'] = data_date[context['date']]

    context['country'] = request.POST.get("country_select") or data_date[context['date']][0]

    context['dates'] = list(data_date.keys())[::-1]
    context['video_id'] = video_id

    context['video'] = data_date_country[(context['date'], context['country'])]
    if context['video']['tags'][0] == '':
        context['video']['tags'] = []

    video_data = exec_query(QUERY_COUNTRY.replace("LABEL", context['country']))
    context['wikidata_country'] = video_data[0]["country"]["value"]

    return render(request, 'base.html', context)
