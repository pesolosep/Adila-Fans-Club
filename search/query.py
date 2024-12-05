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
"""

QUERY_CHANNEL = f"""
    {PREFIXES}

    SELECT ?name ?yearCreated ?subscribers ?rank ?videoViews ?videoCount ?category
	WHERE {{
        :LABEL a :channel;

        {{

            :LABEL  v:createdAt ?yearCreated;
                    v:hasSubscribers ?subscribers;
                    v:trendingRank ?rank;
                    v:videoViews ?videoViews;
                    v:videoCount ?videoCount;
    		        v:fixedName ?name;
                    v:hasCategory ?categoryuri .

            BIND(STRAFTER(STR(?categoryuri), STR(:)) AS ?category)

        }} UNION {{

            :LABEL  v:createdAt ?yearCreated;
        	        v:hasSubscribers ?subscribers;
                    v:videoViews ?videoViews;
                    v:videoCount ?videoCount;
                    v:fixedName ?name .

            BIND("N/A" AS ?category)
            BIND("N/A" AS ?rank)
        }}

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


QUERY_CHANNEL_CATEGORY = f"""
    {PREFIXES}

    SELECT ?id ?yearCreated ?subscribers ?rank ?videoViews ?videoCount ?category
    WHERE {{
        ?id a :channel;
            v:createdAt ?yearCreated;
            v:hasSubscribers ?subscribers;
            v:trendingRank ?rank;
            v:videoViews ?videoViews;
            v:videoCount ?videoCount;
            v:hasCategory ?category;
            rdfs:label LABEL .

        ?category rdfs:label CATEGORY .
    }}
"""

QUERY_VIDEO = f"""
    {PREFIXES}

    SELECT ?title ?thumbs ?desc (GROUP_CONCAT(DISTINCT ?tag; SEPARATOR=", ") AS ?tags) ?colledtedDate ?country ?dailyRank ?viewCount ?likeCount ?commentCount WHERE {{
        LABEL a :video;
        :hasInfoAtTime [
            v:hasTitle ?title;
            v:hasThumbnail ?thumbs;
            v:hasDescription ?desc;
            v:hasTags ?tag
        ];
        v:trendingInfo [
            v:collectedWhen ?colledtedDate;
            v:onCountry ?country;
            v:dailyRank ?dailyRank;
            v:viewCount ?viewCount;
            v:likeCount ?likeCount;
            v:commentCount ?commentCount
        ] .
    }}
    GROUP BY ?title ?thumbs ?desc ?colledtedDate ?country ?dailyRank ?viewCount ?likeCount ?commentCount
"""
