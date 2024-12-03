from urllib.parse import unquote


HOST = "http://127.0.0.1:7200/"

BASE = "http://adilafanclub.com/"
OWL = "http://www.w3.org/2002/07/owl#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
NS1 = "http://xmlns.com/foaf/0.1/"
V = "http://adilafanclub.com/vocab#"
XSD = "http://www.w3.org/2001/XMLSchema#"

REPO_ID = "local_tk"
REPO = f"{HOST}repositories/{REPO_ID}"

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

    SELECT ?id ?yearCreated ?subscribers ?rank ?videoViews ?videoCount ?category
    WHERE {{
        ?id rdfs:label LABEL;
            v:createdAt ?yearCreated;
            v:hasSubscribers ?subscribers;
            v:trendingRank ?rank;
            v:videoViews ?videoViews;
            v:videoCount ?videoCount;
            v:hasCategory ?category .
    }}
"""

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

    SELECT ?id ?title ?thumbs ?desc (GROUP_CONCAT(DISTINCT ?tag; SEPARATOR=", ") AS ?tags) ?colledtedDate ?country ?dailyRank ?viewCount ?likeCount ?commentCount WHERE {{
        ?id a :video;
        v:hasInfoAtTime [
            v:hasTitle LABEL;
            v:hasThumbnail ?thumbs;
            v:hasDescription ?desc;
            v:hasTags  ?tag
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
    GROUP BY ?p ?title ?thumbs ?desc ?colledtedDate ?country ?dailyRank ?viewCount ?likeCount ?commentCount
"""

FUZZY_QUERY = f"""
    {PREFIXES}

    SELECT DISTINCT ?id ?label ?type
    WHERE {{
    	{{
            ?id	a :video;
                v:hasInfoAtTime [v:hasTitle ?label]
            BIND("video" AS ?type)
    	}} UNION {{
        	?id a :channel;
        		rdfs:label ?label .
            BIND("channel" AS ?type)
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
