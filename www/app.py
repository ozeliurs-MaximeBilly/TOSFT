from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import date, timedelta

app = Flask(__name__)

load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    value = db.Column(db.Float)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))


def last30():
    list30 = []
    for i in range(31):
        list30.append((date.today() - timedelta(days=(30-i))).isoformat())
    return list30


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

        existsing_user = User.query.filter_by(username=request.form["username"]).first()

        if existsing_user:
            if existsing_user.password == request.form["password"]:
                flash("You have been logged in !", "success")
                session["id"] = existsing_user.id
                session["username"] = User.query.filter_by(id=session["id"]).first().username
                return redirect(url_for("user"))
            else:
                flash("Wrong Password.", "error")
                return redirect(url_for("login"))
        else:
            flash("Wrong Username.", "error")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existsing_user = User.query.filter_by(username=request.form["username"]).first()

        if existsing_user:
            flash("Username already taken.", "error")
            return redirect(url_for("register"))
        else:
            nusr = User(username=request.form["username"], email=request.form["email"], password=request.form["password"])
            db.session.add(nusr)
            db.session.commit()

            session["id"] = nusr.id
            session["username"] = User.query.filter_by(id=session["id"]).first().username

            flash("You have been registered !", "success")
            return redirect(url_for("user"))
    else:
        return render_template("register.html")


@app.route("/user/", methods=["GET", "POST"])
def user():
    return render_template("user.html")


@app.route("/weight/", methods=["GET", "POST"])
def weight():
    if request.method == "POST":

        return redirect(url_for("weight"))
    else:
        uweight = Weight.query.filter_by(uid=session["id"])
        if uweight:
            for w in uweight:
                print(w.value)
        return render_template("weight.html", labels="'" + "', '".join(last30()) + "'", data="1, 2, 'N/A' , 2.5, 6, 3")


@app.route("/info/")
def info():
    current_user = User.query.filter_by(username=session["username"]).first()
    return render_template("info.html", id=current_user.id, username=current_user.username, email=current_user.email, password=current_user.password)


@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out !", "success")
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
