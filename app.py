from flask import Flask, url_for, redirect, render_template, request
import random
import requests

API_KEY = "AIzaSyB0QuYUYyUzgXbf6_LraR1wTltf4EAyQXs"
API_URL = 'https://www.googleapis.com/books/v1/volumes'
app = Flask(__name__)

active_page = ''
users = {}
public_reviews = {
    "Brandon":"This book is easily one of the best books you'll ever read. For me, a great measure of a good book is one you want to read again. I've read this book 3 times so far. Could not reccomend this book highly enough!",
    "Tom": "What a great Book!",
    "Mark": "Absolutely hated that book!",
} 

# Change this to a list that contains dicts. Atomic would be under title
my_books = [
    {
        'Title':"Atomic Habits",
        'Thoughts': "10/10. I really enjoyed this book, the one percent better idea really stuck with me.",
        "Image" : "static/img/atomic-habits.jpg"
    },
    {
        'Title':"Man's Search For Meaning",
        'Thoughts':"",
        "Image" : "static/img/msfm.jpg"
    },
]

my_wishlist = [
    {
        'Title':"Changing World",
        'Thoughts': "Absolutely brilliant!",
        "Image" : "static/img/changing-world.jpg"
    },
    {
        'Title':"Breath",
        'Thoughts':"Breath taking.",
        "Image" : "static/img/breath.jpg"
    },
     ]

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
    books_length = 0
    if request.method == 'GET':
        search_query = request.args.get('query')

        if search_query:
            api_url = API_URL
            params = {'q': f'intitle:{search_query}', 'key': API_KEY}
            response = requests.get(api_url, params=params)
        
            if response.status_code == 200:
                data = response.json()
                books = data.get('items', [])
                books_length = len(books)
                book_limit = books[:10]

                return render_template("reviews.html", my_books=my_books, active_page=active_page, book_limit=book_limit, books_length=books_length)

    if request.method == 'POST':
        if request.args.get("f") == "f1":
            book_thumbnail = request.form.get('bookThumbnail')
            book_title = request.form.get('bookTitle')
            new_book = {
                'Title': book_title,
                'Thoughts': '',
                'Image': book_thumbnail
            }
            my_books.append(new_book)
            return render_template("reviews.html", my_books=my_books, active_page=active_page, books_length=books_length, book_thumbnail=book_thumbnail)
        
        if request.args.get("f") == "f2":
            book_title = request.form.get('bookTitleRemove')
            for book in my_books:
                if book['Title'] == book_title:
                    my_books.remove(book)
                    return render_template("reviews.html", my_books=my_books, active_page=active_page, books_length=books_length)
        
        if request.args.get("f") == "f3":
            book_title = request.form.get('bookTitleEdit')
            new_thoughts = request.form.get('new_thoughts')
            for book in my_books:
                if book['Title'] == book_title:
                    print(book)
                    print(book['Thoughts'])
                    book['Thoughts'] = new_thoughts
                    return render_template("reviews.html", my_books=my_books, active_page=active_page, books_length=books_length)

    return render_template("reviews.html", my_books=my_books, active_page=active_page, books_length=books_length)

@app.route('/wish_list', methods=['GET', 'POST'])
def wish_list():
    active_page = 'wish_list'
    books_length = 0

    if request.method == 'GET':
        search_query = request.args.get('query')

        if search_query:
            api_url = API_URL
            params = {'q': f'intitle:{search_query}', 'key': API_KEY}
            response = requests.get(api_url, params=params)
        
            if response.status_code == 200:
                data = response.json()
                books = data.get('items', [])
                books_length = len(books)
                book_limit = books[:10]

                return render_template("wish_list.html", my_wishlist=my_wishlist, active_page=active_page, book_limit=book_limit, books_length=books_length)

    if request.method == 'POST':
        if request.args.get("f") == "f1":
            book_thumbnail = request.form.get('bookThumbnail')
            book_title = request.form.get('bookTitle')
            new_book = {
                'Title': book_title,
                'Thoughts': '',
                'Image': book_thumbnail
            }
            my_wishlist.append(new_book)
            return render_template("wish_list.html", my_wishlist=my_wishlist, active_page=active_page, books_length=books_length, book_thumbnail=book_thumbnail)
        
        if request.args.get("f") == "f2":
            book_title = request.form.get('bookTitleRemove')
            for book in my_wishlist:
                if book['Title'] == book_title:
                    my_wishlist.remove(book)
                    return render_template("wish_list.html", my_wishlist=my_wishlist, active_page=active_page, books_length=books_length)
        
        if request.args.get("f") == "f3":
            book_title = request.form.get('bookTitleEdit')
            new_thoughts = request.form.get('new_thoughts')
            for book in my_wishlist:
                if book['Title'] == book_title:
                    print(book)
                    print(book['Thoughts'])
                    book['Thoughts'] = new_thoughts
                    return render_template("wish_list.html", my_wishlist=my_wishlist, active_page=active_page, books_length=books_length)
        
    return render_template("wish_list.html", active_page=active_page, my_wishlist=my_wishlist, books_length=books_length)


if __name__ == '__main__':
    app.run(debug=True, port=8000)