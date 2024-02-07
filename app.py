import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv



def create_app():
    load_dotenv()
    client = MongoClient(os.getenv("MONGODB_URI"))
    app = Flask("__name__")

    app.db = client.microblog



    @app.route("/", methods=["GET", "POST"])
    def home():
    
        if request.method == "POST":
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            entry_content = request.form.get("content")
            app.db.entries.insert_one({"content" : entry_content, "date":formatted_date})

        entries_with_dates = [
        (
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(entry["date"],"%Y-%m-%d").strftime("%b %d")
        ) 
        for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_dates)
    return app