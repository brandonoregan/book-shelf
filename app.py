from flask import Flask, url_for, redirect, render_template, request
import random
import requests

key = "AIzaSyB0QuYUYyUzgXbf6_LraR1wTltf4EAyQXs"
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

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    active_page = 'reviews'
    if request.method == 'GET':
        search_query = request.args.get('query')

        if search_query:
            api_url = 'https://www.googleapis.com/books/v1/volumes'
            params = {'q': f'intitle:{search_query}', 'key': "AIzaSyB0QuYUYyUzgXbf6_LraR1wTltf4EAyQXs"}
            response = requests.get(api_url, params=params)
        
            if response.status_code == 200:
                data = response.json()
                books = data.get('items', [])
                book_limit = books[:10]

                # for book in book_limit:
                #     title = book['volumeInfo']['title']
                #     image_links = book['volumeInfo']['imageLinks']
                #     thumbnail = image_links['thumbnail'] if image_links and 'thumbnail' in image_links else None
                #     small_thumbnail = image_links['smallThumbnail'] if image_links and 'smallThumbnail' in image_links else None

                #     print(f"Title: {title}")
                #     print(f"Thumbnail: {thumbnail}")
                #     print(f"Small Thumbnail: {small_thumbnail}")

                return render_template("reviews.html", personal_reviews=personal_reviews, active_page=active_page, books=book_limit)
            else:
                print(f"API Error - Status Code: {response.status_code}")
                print(f"Error Message: {response.text}")
                return 'ERROR ERROR ERROR'
        
    return render_template("reviews.html", personal_reviews=personal_reviews, active_page=active_page)

@app.route('/wish_list')
def wish_list():
    active_page = 'wish_list'
    return render_template("wish_list.html", active_page=active_page)


if __name__ == '__main__':
    app.run(debug=True, port=8000)