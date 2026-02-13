import os
from flask import Flask, render_template, g, flash, url_for, request, redirect, abort, session
from dotenv import load_dotenv

import sqlite3

DATABASE = "banco.db"
SECRET_KEY = "1234"

load_dotenv() 

app = Flask(__name__)

app.config.from_object(__name__)

def conectar():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = conectar()

@app.teardown_request
def teardown_request(f):
    g.db.close()  

@app.route('/')
def exibir_posts():
    sql = "SELECT titulo, texto, data_criacao from posts ORDER BY id DESC"
    resultado = g.db.execute(sql)
    posts = []

    for titulo, texto, data_criacao in resultado.fetchall():
        posts.append({
            "titulo":titulo,
            "texto":texto,
            "data_criacao":data_criacao
        })

    return render_template('exibir_posts.html', post = posts)   

@app.route("/login", methods = ["POST", "GET"])
def login():
    erro = None
    if(request.method == "POST"):
        if request.form['username' == "Ocean" and request.form['password'] == "1234"]:
            session['logado'] = True
            flash("Usuário logado" + request.form['username'])
            return redirect(url_for('exibir_posts'))
        erro = "Usuário ou senha incorretos"
    return render_template("login.html", erro = erro) 

@app.route("/logout")
def logout():
    return render_template("exibir_posts.html")

    flash("Logout Efetuado")
    return redirect(url_for('exibir_posts'))
 

if __name__ == '__main__':
    app.run(
        host=os.getenv("FLASK_HOST"),
        port=os.getenv("FLASK_PORT"),
        debug=os.getenv("FLASK_DEBUG") == "1"
        )