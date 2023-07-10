from flask import Flask, url_for, redirect, render_template, request

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/reviews')
def reviews():
    return render_template("reviews.html")

@app.route('/wish_list')
def wish_list():
    return render_template("wish_list.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)