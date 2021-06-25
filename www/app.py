from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from datetime import date, timedelta, datetime

app = Flask(__name__)

load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/db.sqlite"
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


def na30():
    list30 = []
    for i in range(31):
        list30.append("'N/A'")
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
        if not "del" in request.form:
            nwei = Weight(date=datetime.strptime(request.form["date"], '%Y-%m-%d').date(), value=request.form["weight"], uid=session["id"])
            db.session.add(nwei)
            db.session.commit()
            return redirect(url_for("weight"))
        else:
            if Weight.query.filter_by(id=request.form["del"]).first().uid == session["id"]:
                db.session.delete(Weight.query.filter_by(id=request.form["del"]).first())
                db.session.commit()
                flash("Weight record has been deleted !","success")
            return redirect(url_for("weight"))
    else:
        na = na30()
        uweight = Weight.query.filter_by(uid=session["id"])
        if uweight:
            for w in uweight:
                if str(w.date) in last30():
                    na[last30().index(str(w.date))] = str(w.value)

        weights = Weight.query.filter_by(uid=session["id"]).order_by(Weight.date.desc())

        return render_template("weight.html", labels="'" + "', '".join(last30()) + "'", data=", ".join(na), weights=weights)


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
    app.run(debug=True, host="0.0.0.0")
