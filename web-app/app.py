from flask import Flask, flash, redirect, url_for, jsonify, request, render_template, send_file, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import time
import datetime

from passlib.hash import sha256_crypt
engine = create_engine("mysql+pymysql://root:@localhost/db_lucky_draw")
# mysql+pymysql://username:password@localhost/databasename

db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.secret_key = b'"F4Q8z\n\xec]/'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# # Required Setup MYSQL data
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_lucky_draw'
# db = SQLAlchemy(app)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(
            ts).strftime('%Y-%m-%d %H:%M:%S')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        secure_password = sha256_crypt.encrypt(str(password))

        usernamedata = db.execute("SELECT username FROM tb_users WHERE username=:username", {
                                  "username": username}).fetchone()
        # usernamedata=str(usernamedata)
        if usernamedata == None:
            if password == confirm_password:
                db.execute("INSERT INTO tb_users(username,password,register_date) VALUES(:username,:password,:register_date)",
                           {"username": username, "password": secure_password, "register_date": timestamp})
                db.commit()
                flash("You are registered and can now login", "success")
                return redirect(url_for('login'))
            else:
                flash("password does not match", "danger")
                return render_template('register.html')
        else:
            flash("user already existed, please login or contact admin", "danger")
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)
        print(password)
        usernamedata = db.execute("SELECT username FROM tb_users WHERE username=:username", {
                                  "username": username}).fetchone()
        passworddata = db.execute("SELECT password FROM tb_users WHERE username=:username", {
                                  "username": username}).fetchone()

        print(usernamedata)
        print(passworddata)
        print(sha256_crypt.hash((request.form.get('password'))))
        if usernamedata is None:
            flash("No username", "danger")
            return render_template("index.html")
        else:
            for passwor_data in passworddata:
                print(password, passwor_data)
                if sha256_crypt.verify(password, passwor_data):
                    session = True
                    flash("You are now logged in!!", "success")

                    # to be edited from here do redict to either svm or home
                    return redirect(url_for("home"))
            else:
                flash("incorrect password", "danger")
                return render_template("index.html")

    return render_template("index.html")


@app.route('/')
def index():
    path = request.path
    return render_template('index.html', data=path)


@app.route('/daftar')
def daftar():
    path = request.path
    return render_template('register.html', data=path)


@app.route('/beranda')
def home():
    path = request.path
    return render_template('home.html', data=path)


@app.route('/peserta')
def participant():
    path = request.path
    return render_template('participant.html', data=path)


@app.route('/hadiah')
def reward():
    path = request.path
    return render_template('reward.html', data=path)


@app.route('/pemenang')
def winner():
    path = request.path
    return render_template('winner.html', data=path)


@app.route('/undian')
def lucky_draw():
    path = request.path
    return render_template('lucky_draw.html', data=path)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
