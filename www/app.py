from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")


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
        flash("You have been logged in !")
        return redirect(url_for("user"))
    else:
        return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def resister():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        flash("You have been registered !")
        return redirect(url_for("user"))
    else:
        return render_template("register.html")


@app.route("/user/")
def user():
    return render_template("info.html")


@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out !")
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(debug=True)
