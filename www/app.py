from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)

# Functions for website rendering
@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["password"] = request.form["password"]
        flash("You have been logged in !", "success")
        return redirect(url_for("user"))
    else:
        return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]

        existsing_user = User.query.filter_by(username=session["username"]).first()

        if existsing_user:
            flash("Username already taken.", "error")
            session.clear()
            return redirect(url_for("register"))
        else:
            nusr = User(username=session["username"], email=session["email"], password=session["password"])
            db.session.add(nusr)
            db.session.commit()

            flash("You have been registered !", "success")
            return redirect(url_for("user"))
    else:
        return render_template("register.html")


@app.route("/user/")
def user():
    return render_template("info.html")


@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out !", "success")
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    if not (db.engine.has_table('user')):
        db.create_all()
    app.run(debug=True)
