from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = "secret key"
# app.config["MONGO_URI"] = "mongodb+srv://ipsita:Ipsita%402023@uk-bd0.u3pngqk.mongodb.net/airbnb"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/property_pricing"
app.config["MONGO_URI"] = "mongodb+srv://zahidhasan:zahid3060@cluster0.3ozgvyw.mongodb.net/Lexical?retryWrites=true&w=majority"
app.config["CORS_HEADERS"] = "Content-Type"
mongo = PyMongo(app)

# cors_add = CORS(app, resources={r"/add": {"origins": "http://localhost:3003"}})