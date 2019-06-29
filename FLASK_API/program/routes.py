from program import app
from flask import render_template, request, redirect, url_for
from datetime import datetime
import requests


@app.route("/")
@app.route("/index")
def index():
    timenow = str(datetime.now())
    return render_template("index.html", time=timenow)


@app.route("/star_wars", methods=["GET", "POST"])
def star_wars():
    attributes = star_wars_menu()

    if request.method == "POST":
        choice = request.form.get("choice")
        return redirect(url_for("star_wars_choice", choice=choice))

    return render_template("starwars.html", attributes=attributes)

@app.route("/star_wars/<choice>")
def star_wars_choice(choice):
    r = requests.get("https://swapi.co/api/" + choice).json()
    results = r["results"]
    return render_template("starwars.html", choice=choice, results=results)
        
def star_wars_menu():
    r = requests.get("https://swapi.co/api/")
    return list(r.json().keys())


    

