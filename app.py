from flask import Flask
from flask import json
from flask import render_template
from flask import request
from flask import session

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from database import select_query
from database import modify_query
from database import create_db

import requests

create_db()

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

app.secret_key = "palabra_super_secreta"


@app.route("/", methods=["GET"])
def index():
    if "username" in session:
        title = "Index"
        return render_template("index.html", title=title, session=session)
    else:
        return login()


@app.route("/members_only", methods=["GET", "POST"])
def members():
    post_id = request.form.get("post_id")
    if "username" in session:
        title = "Members only"
        url = "http://jsonplaceholder.typicode.com/posts"
        response = requests.get(url)
        if response.status_code == 200:
            datasource = json.loads(response.text)
            texto = dict(tuple(post for post in datasource if str(post.get("id")) == str(post_id))[0])
            return render_template("members.html", title=title, session=session, titulo=texto.get('title'), texto=texto.get('body'))
        return {"message": "Service not available"}
    else:
        return index()


@app.route("/login", methods=["GET"])
def login():
    if "username" in session:
        return index()
    else:
        title = "Login"
        return render_template("login.html", title=title)


@app.route("/register", methods=["GET"])
def register():
    if "username" in session:
        return index()
    else:
        title = "Register"
        return render_template("register.html", title=title)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method != "POST":
        return index()
    else:
        user = request.form.get("username").lower()
        password = request.form.get("password")

        username_query = select_query(f"select user_id, username, password from users where username='{user}'")

        print("usename_query: " + str(username_query))

        if username_query:
            if check_password_hash(username_query[0][2], password):
                # Session register
                session["user_id"] = username_query[0][0]
                session["username"] = username_query[0][1]
            else:
                print("Wrong password")
        else:
            print("Wrong username")
        return index()


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method != "POST":
        return index()
    else:
        username = request.form.get("username").lower()
        password = generate_password_hash(request.form.get("password"))

        # Verify if user and email already exist
        username_query = select_query(f"select username from users where username='{username}'")

        if username_query:
            print("User already exists")
            return index()
        elif request.form.get("password") == request.form.get("password2"):
            # Save record DB
            modify_query(f"insert into users (username, password) values ('{username}', '{password}')")

            # Session register
            session["username"] = username

        return index()


@app.route("/validatefield")
def validatefield():
    print(request)
    field = request.args.get("field").lower()
    value = request.args.get("value").lower()
    print(value)
    result = select_query(f"select {field} from users where {field}='{value}'")
    if result:
        print("Value already exists")
        return "Used"
    else:
        print("Value available")
        return "Available"


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return index()


@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Página no encontrada...<h1>"

if __name__ == "__main__":
    app.run(debug=True)