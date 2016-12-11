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
    returner = {}
    connector = sqlite3.connect(PATH)
    connector.row_factory = sqlite3.Row
    form = hashing(form)
    sql = "select * from users where name = '%(username)s'"%form
    con = connector.execute(sql)
    for row in con:
        row = dict(row)
        returner["username"] = True
        if row["password"] == form["password"]:
            returner["password"] = True
            if row["error"] < 3:
                row["error"] = 0
                sql = "update users set error = {error} where name = '{name}'".format(**row)
                con = connector.execute(sql)
        else:
            returner["password"] = False
            row["error"] += 1
            sql = "update users set error = {error} where name = '{name}'".format(**row)
            print sql
            con = connector.execute(sql)
        if row["error"] < 3:
            returner["lock"] = True
        else:
            returner["lock"] = False
        if row["error"] <= 3:
            row["auth"] = returner["password"]
            sql = "insert into {name}(datetime,auth) values(datetime('now'),'{auth}')".format(**row)
            con = connector.execute(sql)
            print sql
        connector.commit()
        connector.close()
        return returner
    returner["username"] = False
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
    sql = "create table %(username)(id integer primary key, datetime text, auth text)"
    con = c.execute(sql)
    con.commit()
    con.close()
    return returner

def getLog(username):
    con = sqlite3.connect(PATH)
    con.row_factory = sqlite3.Row
    sql = "select * from %s"%username
    c = con.execute(sql)
    c = list(map(dict,c))
    return c

if __name__ == "__main__":
    username = "hiroki"
    getLog(username)
