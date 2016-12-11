#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, jsonify
from datetime import timedelta, datetime
import re
from db import login, create, getLog

app = Flask(__name__)
app.secret_key = "AdfivjArifgalfgngav248dgFVifg:p4932hdvs"

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    if session.get("username") is not None:
        return
    elif request.path == "/login" or request.path == "/sign_up" or request.path == "/deny":
        return
    else:
        return redirect("/login")

@app.route("/")
def hello():
    return render_template("welcome.html",name=session["username"])

@app.route("/hello", methods=["POST","GET"])
def hi():
    if request.method == "POST":
        name = request.form["name"]
        return render_template("main.html", name=name)

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    failed = ""
    if request.method == 'POST':
        auth = login(request.form)
        if auth["username"]:
            if auth["lock"]:
                if auth["password"]:
                    session['username'] = request.form['username']
                    return redirect('/')
                else:
                    failed="failed"
            else:
                return redirect("/deny")
        else:
            failed="failed"
    return render_template("login.html", failed=failed)

@app.route("/logout")
def logout():
	session.pop("username", None)
	return redirect("/")

@app.route("/sign_up", methods = ["GET", "POST"])
def signup():
    error = {}
    if request.method == "POST":
        print "hello"
        flg = create(request.form)
        if flg["passwordError"]:
            mess = "Your password must be at least 8 characters."
        else:
            mess = None
        error["password"] = mess
        if flg["usernameError"]:
            mess = "This username is already used."
        else:
            mess = None
        error["username"] = mess
        if flg["againError"]:
            mess = "Passwords must match."
        else:
            mess = None
        error["again"] = mess
        if len(filter(lambda x:type(x) is str, error.values())) == 0:
            session["username"] = request.form["username"]
            return redirect("/")
    print error
    return render_template("signup.html", error=error)

@app.route("/deny", methods = ["GET"])
def deny():
    return render_template("deny.html")

@app.route("/access_log", methods = ["GET"])
def access_log():
    log = getLog(session["username"])
    return render_template("access_log.html", logs=log)

if __name__=="__main__":
	app.run(host="0.0.0.0", port=8080)
