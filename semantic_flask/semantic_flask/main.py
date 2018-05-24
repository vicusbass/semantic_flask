from flask import Flask, render_template
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper2, JSON

app = Flask(__name__)

g = Graph()

sparql = SPARQLWrapper2("http://localhost:8080/rdf4j-server/repositories/bands")


def get_by_genre():
    sparql.setQuery("""
                    prefix : <http://example.org/>
                    prefix foaf: <http://xmlns.com/foaf/0.1/>
                    select ?band ?name
                    where
                    {
                    ?band :style :Prog_metal .
                    ?band  foaf:name  ?name .
                    }
                     """)
    sparql.setReturnFormat(JSON)
    result = sparql.queryAndConvert()
    return result.getValues("band")[0].value, result.getValues("name")[0].value


def list_bands():
    sparql.setQuery("""
                    prefix : <http://example.org/>
                    prefix foaf: <http://xmlns.com/foaf/0.1/>
                    select ?band ?name ?artist ?artistname
                    where
                    {
                    ?band foaf:member ?artist .
                    ?band  foaf:name  ?name .
                    ?artist foaf:name ?artistname .
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
    return render_template("index.html",
                           band=get_by_genre()
                           )


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
