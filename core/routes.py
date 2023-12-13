import json

from flask import (
    render_template, 
    request, 
    flash, 
    redirect, 
    url_for, 
    session
    )

from core import app


def read_data():
    with open("core/static/articles.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_data(data):
    with open("core/static/articles.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def read_users():
    with open("core/static/users.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def write_users(data):
    with open("core/static/users.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


@app.route("/")
def index():
    with open("core/static/articles.json", "r", encoding="utf-8") as file:
        articles = json.load(file)
    return render_template("index.html", articles=articles)


@app.route("/create", methods=["GET", "POST"])
def create():
    with open("core/static/articles.json", "r", encoding="utf-8") as file:
        articles = json.load(file)
    next_id = 1
    if len(articles) > 0:
        next_id = articles[-1]["id"] + 1
    if request.method == "POST":
        new_post = {
            "id": next_id,
            "title": request.form["title"],
            "content": request.form["content"],
        }
        data = read_data()
        data.append(new_post)
        write_data(data)
        flash("Пост был успешно создан", "success")
        return redirect(url_for("index"))
    return render_template("post.html")


@app.route("/articles/<id>")
def article(id):

    f = open("core/static/articles.json", "r")
    articles_str = f.read()
    f.close()
    all_articles = json.loads(articles_str)

    article_by_id = list(filter(lambda x: (x["id"] == int(id)), all_articles))
    article_by_id = article_by_id[0]

    return render_template("post_info.html", article=article_by_id)


@app.route("/articles/edit/<id>", methods=['GET', 'POST'])
def edit(id):

    f = open("core/static/articles.json", "r")
    article_str = f.read()
    f.close()
    all_articles = json.loads(article_str)

    article_by_id = list(filter(lambda x: (x["id"] == int(id)), all_articles))
    article_by_id = article_by_id[0]
    article_index = all_articles.index(article_by_id)

    if request.method == 'POST':
        article_title = request.form["article.title"]
        article_content = request.form["article.content"]
        all_articles[article_index] = {"id": article_by_id["id"], "title": article_title, "content": article_content}

        updated_articles = json.dumps(all_articles)
        f = open("core/static/articles.json", "w")
        f.write(updated_articles)
        f.close()

        return redirect('/')

    return render_template("edit.html", article_id=id, article=article_by_id)


@app.route("/articles/delete")
def delete():

    f = open("core/static/articles.json", "r")
    article_str = f.read()
    f.close()
    all_articles = json.loads(article_str)

    article_id = request.args.get("id")
    article_by_id = list(filter(lambda x: (x["id"] == int(article_id)), all_articles))
    article_by_id = article_by_id[0]
    article_index = all_articles.index(article_by_id)

    del all_articles[article_index]
    updated_clients = json.dumps(all_articles)

    f = open("core/static/articles.json", "w")
    f.write(updated_clients)
    f.close()

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        data = read_users()

        for user in data:
            if user["username"] == username and user["password"] == password:
                session["username"] = username
                flash("Вы успешно вошли", "success")
                return redirect(url_for("index"))
        flash("Неправильное имя или пароль", "danger")
        return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        new_user = {
            "username": request.form["username"],
            "password": request.form["password"],
        }
        data = read_users()
        data.append(new_user)
        write_users(data)
        flash("Вы успешно зарегистрировались", "success")
        login()
        return redirect(url_for("index"))
    return render_template('register.html')
