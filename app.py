from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

account_sid = "ACdf43b7eae4cecf8aa6db09a5bcbf2dd0"
auth_token = "e0959baceff80037daab834e76adb48f"
twilio_phone_number = "+17629851298"
to_number = "+919025792665"

client = Client(account_sid, auth_token)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sarvnnn.sqlite'
app.config['SECRET_KEY'] = 'key'
db.init_app(app)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        Email = request.form["email"]
        Password = request.form["password"]

        user = User.query.filter_by(email = Email).first()

        if user and check_password_hash(user.password, Password):
            session['email'] = Email
            flash("Login Successfull")
            return redirect(url_for('dashboard'))

        else:
            flash("Invaild Credentials. Register First")
            return redirect(url_for('signup'))
    return render_template("login.html")


@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        fname = request.form["first_name"]
        lname = request.form["last_name"]
        email = request.form["email"]
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        user = User(fname = fname, lname = lname, email = email, password = password)

        db.session.add(user)
        db.session.commit()
        flash("Account Created Successfully")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("home.html")

@app.route("/tour")
def tour():
    return render_template("tour.html")

@app.route("/hotel")
def hotel():
    if request.method == "POST":
        s = request.form["search"]
        if s == "Coimbatore":
            return redirect(url_for("coimbatore "))
        else:
            return render_template("hotel.html")
    return render_template("hotel.html")

@app.route("/coimbatore")
def coimbatore():
    return render_template("coimbatore.html")

@app.route("/guide")
def guide():
    return render_template("guide.html")

@app.route("/ar")
def ar():
    return render_template("ar.html")

@app.route("/sos")
def sos():
    return render_template("sos.html")


@app.route('/make_call', methods=['GET','POST'])
def make_call():
    
    try:
        call = client.calls.create(
            url=url_for('handle_call', _external=True),
            to=to_number,
            from_=twilio_phone_number
        )
        return f"Call initiated successfully! SID: {call.sid}"
    except Exception as e:
        return f"Error making call: {str(e)}"


@app.route('/handle_call', methods=['POST'])
def handle_call():
    response = VoiceResponse()
    response.say("Hello! This is a test call from your Flask application.")
    return str(response)

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True)