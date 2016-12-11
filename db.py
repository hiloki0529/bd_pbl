#-*- coding: utf-8 -*-

import sqlite3
import hashlib
import os

PATH = "./db/app.db"

def hashing(form):
    form = dict(form)
    form["password"] = hashlib.sha256(form["password"][0]).hexdigest()
    form["username"] = form["username"][0]
    return form

def login(form):
    connector = sqlite3.connect(PATH)
    c  = connector.cursor()
    form = hashing(form)
    sql = "select * from users where name = '%(username)s'"%form
    con = c.execute(sql)
    for row in con:
        returner = [True]
        if row[2] == form["password"]:
            returner.append(True)
        else:
            returner.append(False)
            sql = "update users set error = %(error)d where '%(username)s"%form
            con = c.excute(sql)
            con.commit()
        return returner
    returner = [False]
    con.close()
    return returner

def create(form):
    returner = {}
    if login(form)[0]:
        userError = False
    else:
        userError = True
    if len(form["password"]) < 8:
        passError = False
    else:
        passError = True
    if form["password"] == form["again"]:
        againError = True
    else:
        againError = False
    returner["usernameError"] = userError
    returner["passwordError"] = passError
    returner["againError"] = againError
    for value in returner.values():
        if not value:
            return returner
    con = sqlite3.connect(PATH)
    c = con.cursor()
    form = hashing(form)
    sql = "insert into users(name,password) values('%(username)s','%(password)s')"%form
    con = c.execute(sql)
    con.commit()
    con.close()
    return returner

if __name__ == "__main__":
    form = {"username":["hirki"], "password":["tani"]}
    print create(form)
