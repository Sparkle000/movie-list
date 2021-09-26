# from logging import FATAL
# from todo.app import Todo
# import re
# from todo.app import Todo
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    rating = db.Column(db.Integer)


@app.route('/')
def index():
    movie_list = Movie.query.all()
    print(movie_list)

    return render_template("base.html", movie_list=movie_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    rating = request.form.get("rating")
    new_movie = Movie(title=title, rating=rating)

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
