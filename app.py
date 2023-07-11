from flask import Flask, url_for, redirect, render_template, request

app = Flask(__name__)

users = {}

@app.route('/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users[username] = password
        print(users)
        return redirect('login')


    return render_template("index.html", user='users')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            return redirect('home')
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