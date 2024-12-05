from urllib.parse import unquote

from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings

HOST = "http://34.173.52.244:7200/"

BASE = "http://adilafanclub.com/"
OWL = "http://www.w3.org/2002/07/owl#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
NS1 = "http://xmlns.com/foaf/0.1/"
V = "http://adilafanclub.com/base/vocab#"
XSD = "http://www.w3.org/2001/XMLSchema#"
WD = "http://www.wikidata.org/entity/"
WDT = "http://www.wikidata.org/prop/direct/"

REPO_ID = "PakAdilaFanClub"
REPO = f"{HOST}repositories/{REPO_ID}"

sparql = SPARQLWrapper(REPO)


def exec_query(query: str) -> dict:
    sparql.setCredentials(settings.DB_UNAME, settings.DB_PASS)
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results["results"]["bindings"]


PREFIXES = f"""
    prefix :      <{BASE}>
    prefix owl:   <{OWL}>
    prefix rdf:   <{RDF}>
    prefix rdfs:  <{RDFS}>
    prefix v:     <{V}>
    prefix ns1:   <{NS1}>
    prefix xsd:   <{XSD}>
    prefix wd:    <{WD}>
    prefix wdt:   <{WDT}>
"""

QUERY_CHANNEL = f"""
    {PREFIXES}

    SELECT ?name ?logo ?yearCreated ?subscribers ?rank ?videoViews ?videoCount ?category
    WHERE {{
        <{BASE}LABEL> a :channel;
        			v:createdAt ?yearCreated;
                    v:hasSubscribers ?subscribers;
                    v:trendingRank ?rank;
                    v:videoViews ?videoViews;
                    v:videoCount ?videoCount;
                    v:fixedName ?name;
                    v:hasCategory ?categoryuri .

        OPTIONAL {{<{BASE}LABEL> v:hasProfile ?logo .}}
		BIND(STRAFTER(STR(?categoryuri), STR(:)) AS ?category)
    }}
"""

QUERY_CHANNEL_VIDEOS = f"""
    {PREFIXES}

    SELECT DISTINCT ?videoID ?title ?desc ?thumb
    WHERE {{
        ?videouri a :video;
            v:createdBy :LABEL ;
            :hasInfoAtTime [
                v:hasTitle ?title;
                v:hasDescription ?desc;
                v:hasThumbnail ?thumb
            ] .

        BIND(STRAFTER(STR(?videouri), STR(:)) AS ?videoID)
    }}

"""

QUERY_VIDEO = f"""
    {PREFIXES}

    SELECT DISTINCT ?title ?desc ?thumb (GROUP_CONCAT(DISTINCT ?tag; SEPARATOR=", ") AS ?tags) ?collectedDate ?country ?weeklyMovement ?dailyMovement ?dailyRank ?viewCount ?likeCount ?commentCount ?language ?datePublished
    WHERE {{
        <{BASE}LABEL> a :video;
            v:trendingInfo ?b1;
            v:publishedWhen ?datePublished;
            v:inLanguage ?language;
            :hasInfoAtTime ?b2 .

        ?b1 v:onCountry ?countryuri;
            v:weeklyMovement ?weeklyMovement;
            v:dailyMovement ?dailyMovement;
            v:dailyRank ?dailyRank;
            v:viewCount ?viewCount;
            v:likeCount ?likeCount;
            v:commentCount ?commentCount;
            v:trendingInfoWhen ?collectedDateuri .

        ?b2 v:hasTitle ?title;
            v:hasDescription ?desc;
            v:hasThumbnail ?thumb .

        OPTIONAL {{?b2 v:hasTags ?taguri .}}
        BIND(STRAFTER(STR(?taguri), STR(:)) as ?tag)
        BIND(STRAFTER(STR(?collectedDateuri), STR(:)) as ?collectedDate)
        BIND(STRAFTER(STR(?countryuri), STR(:)) as ?country)

    }} GROUP BY ?id ?title ?thumb ?desc ?country ?dailyRank ?viewCount ?likeCount ?commentCount ?weeklyMovement ?dailyMovement ?collectedDate ?language ?datePublished
"""

FUZZY_QUERY = f"""
    {PREFIXES}

    SELECT DISTINCT ?id ?label ?type
    WHERE {{
        {{
            ?uri a :video;
                 :hasInfoAtTime [v:hasTitle ?label]
            BIND("video" AS ?type)
        }} UNION {{
            ?uri a :channel;
                        v:fixedName ?label .
            BIND("channel" AS ?type)
        }}

        BIND(STRAFTER(STR(?uri), STR(:)) AS ?id)
        FILTER(STRSTARTS(LCASE(?label), LCASE("LABEL")) || CONTAINS(LCASE(?label), LCASE("LABEL")))

    }} LIMIT 1000
"""

QUERY_COUNTRY = f"""
    {PREFIXES}

    SELECT ?country WHERE {{
        SERVICE <https://query.wikidata.org/sparql> {{
            ?country wdt:P297 LABEL;
        }}
    }}
"""


def fix_encoding(data: str) -> str:
    data = unquote(data).encode()

    # GRAPHDB WHY DO YOU DO THIS TO ME
    data = data.decode('utf-8')
    data = data.encode('latin1')
    data = data.decode('utf-8')
    data = data.encode('latin1')
    data = data.decode('utf-8')
    data = data.encode('latin1')
    data = data.decode('utf-8')
    data = data.encode('latin1')
    data = data.decode('utf-8')

    return data
