from flask import Flask, url_for, redirect, render_template, request
import random
app = Flask(__name__)

active_page = ''
users = {}
public_reviews = {
    "Brandon":"This book is easily one of the best books you'll ever read. For me, a great measure of a good book is one you want to read again. I've read this book 3 times so far. Could not reccomend this book highly enough!",
    "Tom": "What a great Book!",
    "Mark": "Absolutely hated that book!",
} 

# Change this to a list that contains dicts. Atomic would be under title
personal_reviews = {
    "Atomic Habits" : 
    {
        "Thoughts" : "10/10. I really enjoyed this book, the one percent better idea really stuck with me.", 
        "img" : "atomic-habits.jpg"
        },
    "Man's Search For Meaning" : 
    {
        "Thoughts":"10/10 Core them of the book, he who has a strong enough why can overcome anything.",
        "img" : "msfm.jpg"
        }
}

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
        current_user = username
        if username in users and users[username] == password:
            print(f"current_user = {current_user}")
            return redirect('home')
    return render_template("login.html")

@app.route('/home', methods = ['GET', 'POST'])
def home():
    active_page = 'home'
    current_user = f'User{random.randint(0,5000)}'
    if request.method == "POST":
        review = request.form.get('review')
        public_reviews[current_user] = review
        print(public_reviews)
        return render_template("home.html", public_reviews = public_reviews)
        

    return render_template("home.html", public_reviews = public_reviews, active_page=active_page)

@app.route('/reviews')
def reviews():
    active_page = 'reviews'
    return render_template("reviews.html", personal_reviews=personal_reviews, active_page=active_page)

@app.route('/wish_list')
def wish_list():
    active_page = 'wish_list'
    return render_template("wish_list.html", active_page=active_page)


if __name__ == '__main__':
    app.run(debug=True, port=8000)