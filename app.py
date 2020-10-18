import os
from flask import Flask, session,render_template,request,redirect,url_for,flash,make_response,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload')
def uploadpage():
    return render_template("uploadpage.html")

@app.route('/imgupload',methods=["POST"])
def imgupload():
    try:
        data = request.get_json()
        imagename = data["imagename"]
        artistname = data["artistname"]
        url = data["downloadurl"]
        db.execute("INSERT INTO image (name,artist,link) VALUES (:n, :a, :l)",{"n":imagename,"a":artistname,"l":url})
        db.commit()
    except:
        data = None
    return jsonify({"message":"Successful"})
