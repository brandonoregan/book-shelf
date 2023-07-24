from flask import Flask, url_for, redirect, render_template, request, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from datetime import datetime
import requests


API_KEY = "AIzaSyB0QuYUYyUzgXbf6_LraR1wTltf4EAyQXs"
API_URL = "https://www.googleapis.com/books/v1/volumes"

app = Flask(__name__)
app.secret_key = "123456789"

active_page = ""
users = []
slider_showing = False

login_manager = LoginManager()
login_manager.login_view = "render_login"
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def is_active(self):
        return True

    def get_id(self):
        return str(self.user_id)


# Mini Database code (Example website display key and values)

# Contains default reviews for display purposes
public_reviews = {
    "Brandon": "This book is easily one of the best books you'll ever read. For me, a great measure of a good book is one you want to read again. I've read this book 3 times so far. Could not reccomend this book highly enough!",
    "Tom": "What a great Book!",
    "Mark": "Absolutely hated that book!",
}

# Contains default books for display purposes
my_books = [
    {
        "Title": "Atomic Habits",
        "Thoughts": "10/10. I really enjoyed this book, the one percent better idea really stuck with me.",
        "Image": "static/img/atomic-habits.jpg",
    },
    {
        "Title": "Man's Search For Meaning",
        "Thoughts": "",
        "Image": "static/img/msfm.jpg",
    },
]

# Contains default book for display purposes
my_wishlist = [
    {
        "Title": "Principles for Navigating Big Debt Crisis",
        "Image": "static/img/changing-world.jpg",
        "Description": "Ray Dalio, the legendary investor and international bestselling author of Principles - whose books have sold more than five million copies worldwide - shares his unique template for how debt crises work and principles for dealing with them well. This template allowed his firm, Bridgewater Associates, to antic-ipate 2008s events and navigate them well while others struggled badly. As he explained in his international best-seller Principles , Ray Dalio believes that almost everything happens over and over again through time, so that by studying patterns one can understand the cause-effect relationships behind events and develop principles for dealing with them well. In this three-part research series, he does just that for big debt crises and shares his template in the hopes of reducing the chances of big debt crises hap-pening and helping them be better managed in the future. The template comes in three parts: 1. The Archetypal Big Debt Cycle (which explains the template) 2. Three Detailed Cases (which examines in depth the 2008 financial crisis, the 1930s Great Depression and the 1920s infla-tionary depression of Germanys Weimar Republic) 3. Compendium of 48 Cases (which is a compendium of charts and brief descriptions of the worst debt crises of the last 100 years) Whether youre an investor, a policy maker, or are simply interested in debt, this unconventional perspective from one of the few people who navigated the crisis successfully, Principles for Navigating Big Debt Crises will help you understand the economy and markets in revealing new ways.  ",
    },
    {
        "Title": "Breath",
        "Image": "static/img/breath.jpg",
        "Description": "A New York Times Bestseller A Washington Post Notable Nonfiction Book of 2020 Named a Best Book of 2020 by NPR   'A fascinating scientific, cultural, spiritual and evolutionary history of the way humans breathe-and how we've all been doing it wrong for a long, long time.' -Elizabeth Gilbert, author of Big Magic and Eat Pray Love No matter what you eat, how much you exercise, how skinny or young or wise you are, none of it matters if you're not breathing properly. There is nothing more essential to our health and well-being than breathing: take air in, let it out, repeat twenty-five thousand times a day. Yet, as a species, humans have lost the ability to breathe correctly, with grave consequences. Journalist James Nestor travels the world to figure out what went wrong and how to fix it. The answers aren't found in pulmonology labs, as we might expect, but in the muddy digs of ancient burial sites, secret Soviet facilities, New Jersey choir schools, and the smoggy streets of São Paulo. Nestor tracks down men and women exploring the hidden science behind ancient breathing practices like Pranayama, Sudarshan Kriya, and Tummo and teams up with pulmonary tinkerers to scientifically test long-held beliefs about how we breathe. Modern research is showing us that making even slight adjustments to the way we inhale and exhale can jump-start athletic performance; rejuvenate internal organs; halt snoring, asthma, and autoimmune disease; and even straighten scoliotic spines. None of this should be possible, and yet it is. Drawing on thousands of years of medical texts and recent cutting-edge studies in pulmonology, psychology, biochemistry, and human physiology, Breath turns the conventional wisdom of what we thought we knew about our most basic biological function on its head. You will never breathe the same again.",
    },
]

# Functions


@login_manager.user_loader
def load_user(user_id):
    user_id = int(user_id)
    for user in users:
        if user.user_id == user_id:
            return user
    return None


def handle_api(search_query):
    """Handle search query API respone"""
    api_url = API_URL
    params = {"q": f"intitle:{search_query}", "key": API_KEY}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        books = data.get("items", [])
        book_limit = books[:10]
        slider_showing = True
        return book_limit, slider_showing
    else:
        return 0, []


# Flask route/route functions

@app.route("/")
def render_index():
    """Renders associated template"""
    active_page = 'sign_up'

    return render_template("index.html", active_page=active_page, user=current_user)

@app.route("/sign_up")
def render_register():
    """Renders associated template"""
    active_page = "sign_up"

    return render_template("sign_up.html", active_page=active_page, user=current_user)


@app.route("/sign_up", methods=["POST"])
def add_user():
    """Creates and stores new user"""
    username = request.form.get("username")
    password = request.form.get("password")
    user_id = len(users)
    new_user = User(username=username, password=password, user_id=user_id)
    users.append(new_user)
    login_user(new_user, remember=True)
    return redirect(url_for("render_home"))


@app.route("/login")
def render_login():
    """Renders associated template"""
    active_page = "login"
    return render_template("login.html", active_page=active_page, user=current_user)


@app.route("/login", methods=["POST"])
def login():
    """Handles user authentication"""
    username = request.form.get("username")
    password = request.form.get("password")
    user = None
    for user_info in users:
        if user_info.username == username:
            user = user_info
            print(user)
            break

    if user and user.password == password:
        login_user(user, remember=True)
        return redirect(url_for("render_home"))
    else:
        flash(
            "Invalid username or password. Please check your credentials and try again."
        )
        return render_template("login.html", user=current_user)


@app.route("/logout")
@login_required
def logout():
    """Renders associated template"""
    logout_user()
    return redirect(url_for("render_login"))


@app.route("/home")
@login_required
def render_home():
    """Renders associated template"""

    active_page = "home"

    return render_template(
        "home.html",
        public_reviews=public_reviews,
        active_page=active_page,
        user=current_user,
    )


@app.route("/home", methods=["POST"])
def home():
    """Handles review creation and storage"""
    active_page = "home"
    review = request.form.get("review")

    if current_user.is_authenticated:
        username = current_user.username
        formatted_time = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        key = f"{username} - {formatted_time}"
        public_reviews[key] = review
        return render_template(
            "home.html",
            public_reviews=public_reviews,
            active_page=active_page,
            user=current_user,
        )
    else:
        flash("You need to log in to access this page.")
        return redirect(url_for("render_login"))


@app.route("/reviews")
def render_reviews():
    """Handles display of approriate API results"""
    active_page = "reviews"
    slider_showing = False
    search_query = request.args.get("query")

    if search_query:
        book_limit, slider_showing = handle_api(search_query)

        return render_template(
            "reviews.html",
            my_wishlist=my_wishlist,
            active_page=active_page,
            book_limit=book_limit,
            slider_showing=slider_showing,
            my_books=my_books,
            user=current_user,
        )
    else:
        book_limit = []
        return render_template(
            "reviews.html",
            active_page=active_page,
            my_wishlist=my_wishlist,
            slider_showing=slider_showing,
            my_books=my_books,
            user=current_user,
        )


@app.route("/reviews", methods=["POST"])
def reviews():
    """Handle each post request of the reviews function"""
    active_page = "reviews"

    if request.args.get("f") == "f1":
        book_thumbnail = request.form.get("bookThumbnail")
        book_title = request.form.get("bookTitle")
        new_book = {
            "Title": book_title,
            "Thoughts": "",
            "Image": book_thumbnail,
        }
        my_books.append(new_book)
        return render_template(
            "reviews.html",
            my_books=my_books,
            active_page=active_page,
            book_thumbnail=book_thumbnail,
            user=current_user,
        )

    if request.args.get("f") == "f2":
        book_title = request.form.get("bookTitleRemove")
        for book in my_books:
            if book["Title"] == book_title:
                my_books.remove(book)
                return render_template(
                    "reviews.html",
                    my_books=my_books,
                    active_page=active_page,
                    user=current_user,
                )

    if request.args.get("f") == "f3":
        book_title = request.form.get("bookTitleEdit")
        new_thoughts = request.form.get("new_thoughts")
        for book in my_books:
            if book["Title"] == book_title:
                book["Thoughts"] = new_thoughts
                return render_template(
                    "reviews.html",
                    my_books=my_books,
                    active_page=active_page,
                    user=current_user,
                )


@app.route("/wish_list")
def render_wish_list():
    """Handles display of approriate API results"""

    active_page = "wish_list"
    search_query = request.args.get("query")
    slider_showing = False

    if search_query:
        book_limit, slider_showing = handle_api(search_query)

        return render_template(
            "wish_list.html",
            my_wishlist=my_wishlist,
            active_page=active_page,
            book_limit=book_limit,
            slider_showing=slider_showing,
            user=current_user,
        )
    else:
        book_limit = []
        return render_template(
            "wish_list.html",
            active_page=active_page,
            my_wishlist=my_wishlist,
            slider_showing=slider_showing,
            user=current_user,
        )


@app.route("/wish_list", methods=["POST"])
def wish_list():
    """Handle each post request of the wish_list function"""
    active_page = "wish_list"

    if request.args.get("f") == "f1":
        book_thumbnail = request.form.get("bookThumbnail")
        book_title = request.form.get("bookTitle")
        book_description = request.form.get("bookDescription")
        new_book = {
            "Title": book_title,
            "Image": book_thumbnail,
            "Description": book_description,
        }
        my_wishlist.append(new_book)
        return render_template(
            "wish_list.html",
            my_wishlist=my_wishlist,
            active_page=active_page,
            book_thumbnail=book_thumbnail,
            user=current_user,
        )

    if request.args.get("f") == "f2":
        book_title = request.form.get("bookTitleRemove")
        for book in my_wishlist:
            if book["Title"] == book_title:
                my_wishlist.remove(book)
                return render_template(
                    "wish_list.html",
                    my_wishlist=my_wishlist,
                    active_page=active_page,
                    user=current_user,
                )
        return render_template(
            "wish_list.html",
            my_wishlist=my_wishlist,
            active_page=active_page,
            user=current_user,
        )


if __name__ == "__main__":
    app.run(debug=True, port=8000)
