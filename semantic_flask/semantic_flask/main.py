from flask import Flask, render_template, request, redirect, url_for
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper2, JSON

app = Flask(__name__)

g = Graph()

sparql = SPARQLWrapper2("http://localhost:8080/rdf4j-server/repositories/bands")


def list_genres():
    sparql.setQuery("""
                    PREFIX dc: <http://purl.org/dc/elements/1.1/>
                    PREFIX mo: <http://purl.org/ontology/mo/>
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    select ?genre ?genretitle
                    where
                    {
                        ?genre rdfs:subClassOf mo:Genre .
                        ?genre dc:title ?genretitle .
                    }
                    ORDER BY ?genretitle
                     """)
    sparql.setReturnFormat(JSON)
    result = sparql.queryAndConvert()
    return sparql.query().bindings


def list_bands():
    sparql.setQuery("""
                    prefix : <http://example.org/>
                    prefix foaf: <http://xmlns.com/foaf/0.1/>
                    prefix dc: <http://purl.org/dc/elements/1.1/>
                    prefix schema: <http://schema.org/>
                    select distinct ?band ?name ?logo ?style ?stylename
                    where
                    {
                    ?band foaf:member ?artist .
                    ?band  foaf:name  ?name .
                    ?band schema:logo ?logo .
                    ?band :style ?style .
                    ?style dc:title ?stylename .
                    }
                     """)
    sparql.setReturnFormat(JSON)
    result = sparql.queryAndConvert()
    return sparql.query().bindings


def list_artists():
    sparql.setQuery("""
        PREFIX mo: <http://purl.org/ontology/mo/>
        PREFIX schema: <http://schema.org/>
        PREFIX : <http://example.org/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?artist ?predicate ?band ?artistname ?bandname
        WHERE{
          ?artist a mo:MusicArtist .
          ?artist ?predicate ?band .
          ?band rdf:type schema:MusicGroup .
          ?artist foaf:name ?artistname .
          ?band foaf:name ?bandname .
        }
        ORDER BY ?band ASC(?predicate)
    """)
    sparql.setReturnFormat(JSON)
    result = sparql.queryAndConvert()
    return sparql.query().bindings


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/bands")
def bands_page():
    return render_template("bands.html",
                           bands=list_bands()
                           )


@app.route("/artists")
def artists_page():
    return render_template("artists.html",
                           artists=list_artists()
                           )


@app.route("/addband")
def addband_page():
    return render_template("addband.html",
                           genres=list_genres()
                           )


@app.route('/result', methods=['POST'])
def result_band_added():
    if request.method == 'POST':
        sparql_insert = SPARQLWrapper2("http://localhost:8080/rdf4j-server/repositories/bands/statements")
        result = request.form
        band_name = result["band_name"]
        style = result["style"]
        activity_started = result["activity_started"] + "-01-01T00:00:00Z"
        logo_url = result["logo_url"]
        query = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX : <http://example.org/> 
            PREFIX schema: <http://schema.org/>
            PREFIX mo: <http://purl.org/ontology/mo/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            INSERT DATA 
            {{GRAPH :Bands
            {{:{} foaf:name '{}';
                       rdf:type schema:MusicGroup;
                       mo:activity_start '{}';
                       schema:logo '{}';
                       :style '{}' .
            }}
            }}""".format(band_name.replace(" ", ""), band_name, activity_started, logo_url, style)
        print(query)
        sparql_insert.setQuery(query)
        sparql_insert.method = 'POST'
        print(sparql_insert.query())
        return redirect(url_for('bands_page'))
