from flask import Flask, render_template
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper2, JSON

app = Flask(__name__)

g = Graph()

# result = g.parse("semantic_flask/static/rdf/bands.trig", format="trig")
sparql = SPARQLWrapper2("http://localhost:8080/rdf4j-server/repositories/music")


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
    print(result.getValues("band")[0].value)
    print(result.getValues("name")[0].value)
    return result.getValues("band")[0].value, result.getValues("name")[0].value


@app.route("/")
def home_page():
    return render_template("index.html",
                           band=get_by_genre()
                           )
