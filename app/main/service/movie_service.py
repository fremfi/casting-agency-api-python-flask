import datetime

from app.main import db
from app.main.model.movie import Movie


def get_movies(page, per_page):
    return (Movie.query.order_by(Movie._title.desc()).
            paginate(page, per_page, error_out=False))


def get_movie(movie_id):
    return Movie.query.get(movie_id)


def post_movie(title, release_date):
    movie = Movie(
        title=title,
        release_date=release_date,
    )
    movie.insert()
    return movie


def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        movie.delete()
    return movie


def update_movie(movie_id, title, release_date):
    movie = Movie.query.get(movie_id)
    if movie:
        movie.title = title or movie.title
        movie.release_date = (release_date or
                              movie.release_date.strftime('%Y-%m-%d'))
        movie.update()

    return movie
