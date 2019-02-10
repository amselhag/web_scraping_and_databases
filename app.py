from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mar

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    data_scraped = mongo.db.data_scraped.find_one()

    # Return template and data
    return render_template("index.html", data_scraped=data_scraped)


# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():
   
    data_scraped = mongo.db.data_scraped

     # Run the scrape function
    data = scrape_mar.scrape_info()

    # Update the Mongo database using update and upsert=True
    data_scraped.update({}, data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)