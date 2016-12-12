#-*- coding: utf-8 -*-

import sqlite3
import hashlib
import os
import random
import datetime

PATH = os.path.join(os.path.dirname(__file__),"db/app.db")

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
            con = connector.execute(sql)
        if row["error"] < 3:
            returner["lock"] = True
        else:
            returner["lock"] = False
        if row["error"] <= 3:
            row["auth"] = returner["password"]
            row["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "insert into {name}(datetime,auth) values('{datetime}','{auth}')".format(**row)
            con = connector.execute(sql)
        connector.commit()
        connector.close()
        return returner
    returner["username"] = False
    return returner

def create(form):
    returner = {}
    if check(form["username"]):
        userError = False
    else:
        userError = True
    if len(form["password"]) > 7:
        passError = False
    else:
        passError = True
    if form["password"] == form["again"]:
        againError = False
    else:
        againError = True
    returner["usernameError"] = userError
    returner["passwordError"] = passError
    returner["againError"] = againError
    for value in returner.values():
        if value: 
            return returner
    con = sqlite3.connect(PATH)
    form = hashing(form)
    sql = "insert into users(name,password) values('%(username)s','%(password)s')"%form
    con.execute(sql)
    sql = "create table %(username)s (id integer primary key, datetime text, auth text)"%form
    con.execute(sql)
    con.commit()
    con.close()
    return returner

def check(username):
    con = sqlite3.connect(PATH)
    sql = "select * from users where name = '%s'"%username
    c = con.execute(sql)
    for v in c:
        return False
    return True

def getLog(username):
    con = sqlite3.connect(PATH)
    con.row_factory = sqlite3.Row
    sql = "select * from %s"%username
    c = con.execute(sql)
    c = list(map(dict,c))
    return c

def getPic():
    con = sqlite3.connect(PATH)
    con.row_factory = sqlite3.Row
    sql = "select max(id) from pic_auth"
    c = con.execute(sql)
    id_max = c.fetchone()
    id_max = id_max[0]
    id = random.randint(1,id_max)
    sql = "select * from pic_auth where id = %d"%id
    c = con.execute(sql)
    row = dict(c.fetchone())
    return row

if __name__ == "__main__":
    pic_auth()
