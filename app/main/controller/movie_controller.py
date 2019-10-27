import app.main.service
from flask import request
from flask_restplus import abort
from sqlalchemy import exc
from app.main.service import movie_service
from app.main.exceptions import ValidationError
from flask_restplus import Resource
from ..util.dto import MovieDto
from werkzeug.exceptions import (BadRequest, NotFound, InternalServerError,
                                 Unauthorized, Forbidden, MethodNotAllowed)
from app.main.auth.auth import requires_auth

MOVIES_PER_PAGE = 10
api = MovieDto.api
_movie = MovieDto.movie
_error = MovieDto.error


@api.route('/')
class MovieList(Resource):
    @api.doc('list_of_movies')
    @api.marshal_list_with(_movie, envelope='movies')
    @requires_auth('get:movies')
    def get(payload, self):
        """
        get_movies: fetches movies
        Args:
            page (data type: int)
        Returns:
            returns an array of movies
        """

        page = request.args.get('page', 1, type=int)
        moviesPagination = (movie_service.
                            get_movies(page, MOVIES_PER_PAGE))
        movies = moviesPagination.items
        formatted_movies = [movie.format() for movie in movies]

        if not len(movies):
            raise NotFound({
                "status": 404,
                "description": "No movies were found on page " + str(page)
            })

        return formatted_movies

    @api.doc('create a new movie')
    @api.expect(_movie, validate=True)
    @api.marshal_with(_movie)
    @requires_auth('create:movie')
    def post(payload, self):
        """
        create_movie: creates a new movie
        Args:
            title (data type: str)
            release_date (data type: str)
        Returns:
            returns the newly created movie
        """
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            movie = movie_service.post_movie(title, release_date)
        except ValidationError as exc:
            raise BadRequest({
                "status": 400,
                "description": exc.error
            })
        except exc.SQLAlchemyError:
            abort(500)

        return movie.format(), 201


@api.route('/<movie_id>')
@api.param('movie_id', 'Movie identifier')
class Movie(Resource):
    @api.doc('get a movie by id')
    @api.marshal_with(_movie)
    @requires_auth('get:movies')
    def get(payload, self, movie_id):
        """
        get_movie: get a movie by id
        Args:
            movie_id (data type: int)
        Returns:
            returns movie
        """
        movie = movie_service.get_movie(movie_id)

        if not movie:
            raise NotFound({
                "status": 404,
                "description": "Movie with id " +
                movie_id + " was not found"
            })

        return movie.format()
  
    @api.doc('delete a movie by id')
    @requires_auth('delete:movie')
    def delete(payload, self, movie_id):
        """
        delete_movie: deletes a movie by id
        Args:
            movie_id (data type: int)
        Returns:
            returns success if the movie is deleted
        """
        try:
            deleted_movie = movie_service.delete_movie(movie_id)
            if not deleted_movie:
                raise NotFound({
                    "status": 404,
                    "description": "Movie with id " +
                    movie_id + " was not found"
                })
        except exc.SQLAlchemyError:
            abort(500)
        return '', 204

    @api.doc('update a movie by id')
    @api.marshal_with(_movie)
    @requires_auth('update:movie')
    def patch(payload, self, movie_id):
        """
        update_movie: updates a movie given id
        Args:
            title (data type: str) optional 
            release_date (data type: str) optional
        Returns:
            returns success if the movie is updated
        """
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            updated_movie = (movie_service.
                             update_movie(movie_id, title, release_date))
            if not updated_movie:
                raise NotFound({
                    "status": 404,
                    "description": "Movie with id " +
                    movie_id + " was not found"
                })
        except ValidationError as exc:
            raise BadRequest({
                "status": 400,
                "description": exc.error
            })
        return updated_movie.format(), 200


@api.errorhandler(BadRequest)
@api.marshal_with(_error, code=400, envelope='error')
def handle_bad_request(error):
    '''BadRequest Error Handling'''
    return error.description, 400


@api.errorhandler(NotFound)
@api.marshal_with(_error, code=404, envelope='error')
def handle_not_found(error):
    '''NotFound Error Handling'''
    return error.description, 404


@api.errorhandler(MethodNotAllowed)
@api.marshal_with(_error, code=405, envelope='error')
def handle_not_found(error):
    '''NotFound Error Handling'''
    return {
        "status": 405,
        "description": "Method Not Allowed"
    }, 405


@api.errorhandler(Forbidden)
@api.marshal_with(_error, code=403, envelope='error')
def handle_not_found(error):
    '''NotFound Error Handling'''
    return {
        "status": 403,
        "description": "Forbidden"
    }, 403


@api.errorhandler(Unauthorized)
@api.marshal_with(_error, code=401, envelope='error')
def handle_bad_request(error):
    '''BadRequest Error Handling'''
    return {
        "status": 401,
        "description": "Unauthorized"
    }, 401


@api.errorhandler(InternalServerError)
@api.marshal_with(_error, code=500, envelope='error')
def handle_not_found(error):
    '''NotFound Error Handling'''
    return {
        "status": 500,
        "description": "Internal Server Error"
    }, 500
