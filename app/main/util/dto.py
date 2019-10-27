from flask_restplus import Namespace, fields


class MovieDto:
    api = Namespace('Movie', description='get, post, update movies')
    movie = api.model('movie', {
        'id': fields.Integer(description="movie id"),
        'title': fields.String(required=True, description='movie title'),
        'release_date': (fields.Date(required=True,
                         description='movie release date'))
    })
    error = api.model('error', {
        'status': fields.Integer(required=True, description='status code'),
        'description': fields.String(required=True, description='error'),
    })


class ActorDto:
    api = Namespace('Actor', description='get, post, update actors')
    actor = api.model('actor', {
        'id': fields.Integer(description="actor id"),
        'name': fields.String(required=True, description='actor name'),
        'age': fields.Integer(required=True, description="actor age"),
        'gender': fields.String(required=True, description='actor gender'),
    })
    error = api.model('error', {
        'status': fields.Integer(required=True, description='status code'),
        'description': fields.String(required=True, description='error'),
    })
