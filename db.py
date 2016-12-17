#-*- coding: utf-8 -*-

import sqlite3
import hashlib
import os
import random
import datetime
import uuid
from twitter import send_DM

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
        returner["token"] = createToken()
        returner["username"] = True
        if row["password"] == form["password"]:
            returner["password"] = True
            if row["error"] < 3:
                row["error"] = 0
                row["token"] = returner["token"]
                sql = "update users set error = {error} where name = '{name}'".format(**row)
                con = connector.execute(sql)
                sql = "update users set token = '{token}' where name = '{name}'".format(**row)
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
    token = createToken()
    form.update({"token":token})
    sql = "insert into users(name,password,token) values('%(username)s','%(password)s','%(token)s')"%form
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

def putCode(token,code):
    con = sqlite3.connect(PATH)
    con.row_factory = sqlite3.Row
    sql = "update users set code = '%s' where token = '%s'"%(code,token)
    c = con.execute(sql)
    con.commit()
    sql = "select twitter from users where token = '%s'"%token
    c = con.execute(sql)
    for row in c:
        text = "Your code is %s."%code
        send_DM(row["twitter"],text)
    con.close()

def step2(token, code):
    con = sqlite3.connect(PATH)
    con.row_factory = sqlite3.Row
    sql = "select code from users where token = '%s'"%token
    print sql
    c = con.execute(sql)
    for row in c:
        if row["code"] == code:
            con.close()
            return True
        else:
            return False

def getUsername(token):
    con = sqlite3.connect(PATH)
    con.row_factory = sqlite3.Row
    sql = "select name from users where token = '%s'"%token
    c = con.execute(sql)
    for row in c:
        sql = "update users set token = '' where token = '%s'"%token
        con.execute(sql)
        con.commit()
        con.close()
        return row["name"]

def createToken():
    return hashlib.md5( str(uuid.uuid4()) ).hexdigest()

if __name__ == "__main__":
    pic_auth()
