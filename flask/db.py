#-*- coding: utf-8 -*-

import sqlite3
import hashlib

PATH = "db/app.db"

def hashing(form):
    form = dict(form)
    for key,value in form.items():
        form[key] = hashlib.sha256(value[0]).hexdigest()
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
        return returner
    returner = [False]
    return returner

def create(form):
    if login(form)[0]:
        return False
    if len(form["password"]) > 8:
        return False
    con = sqlite3.connect(PATH)
    c = con.cursor()
    form = hashing(form)
    sql = "insert into users(name,password) values('%(username)s','%(password)s')"%form
    con = c.execute(sql)
    con.commit()
    con.close()

if __name__ == "__main__":
    form = {"username":["hiroki"], "password":["tani"]}
    print login(form)
