import app.main.service
from flask import request
from flask_restplus import abort
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from app.main.service import actor_service
from app.main.exceptions import ValidationError
from flask_restplus import Resource
from ..util.dto import ActorDto
from werkzeug.exceptions import (BadRequest, NotFound, InternalServerError,
                                 Unauthorized, Forbidden, MethodNotAllowed)
from app.main.auth.auth import requires_auth

ACTORS_PER_PAGE = 10
api = ActorDto.api
_actor = ActorDto.actor
_error = ActorDto.error


@api.route('/')
class ActorList(Resource):
    @api.doc('list_of_actors')
    @api.marshal_list_with(_actor, envelope='actors')
    @requires_auth('get:actors')
    def get(payload, self):
        """
        get_actors: fetches actors
        Args:
            page (data type: int)
        Returns:
            returns an array of actors
        """

        page = request.args.get('page', 1, type=int)
        actorsPagination = (actor_service.
                            get_actors(page, ACTORS_PER_PAGE))
        actors = actorsPagination.items
        formatted_actors = [actor.format() for actor in actors]

        if not len(actors):
            raise NotFound({
                "status": 404,
                "description": "No actors were found on page " + str(page)
            })

        return formatted_actors

    @api.doc('create a new actor')
    @api.expect(_actor, validate=True)
    @api.marshal_with(_actor)
    @requires_auth('create:actor')
    def post(payload, self):
        """
        create_actor: creates a new actor
        Args:
            name (data type: str)
            age (data type: int)
            gender (data type: str)
        Returns:
            returns the newly created actor
        """
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            actor = actor_service.post_actor(name, age, gender)
        except ValidationError as exc:
            raise BadRequest({
                "status": 400,
                "description": exc.error
            })
        except (DBAPIError, SQLAlchemyError):
            abort(500)

        return actor.format(), 201


@api.route('/<actor_id>')
@api.param('actor_id', 'Actor identifier')
class Actor(Resource):
    @api.doc('get a actor by id')
    @api.marshal_with(_actor)
    @requires_auth('get:actors')
    def get(payload, self, actor_id):
        """
        get_actor: get a actor by id
        Args:
            actor_id (data type: int)
        Returns:
            returns actor
        """
        actor = actor_service.get_actor(actor_id)

        if not actor:
            raise NotFound({
                "status": 404,
                "description": "Actor with id " +
                actor_id + " was not found"
            })

        return actor.format()

    @api.doc('delete a actor by id')
    @requires_auth('delete:actor')
    def delete(payload, self, actor_id):
        """
        delete_actor: deletes a actor by id
        Args:
            actor_id (data type: int)
        Returns:
            returns success if the actor is deleted
        """
        try:
            deleted_actor = actor_service.delete_actor(actor_id)
            if not deleted_actor:
                raise NotFound({
                    "status": 404,
                    "description": "Actor with id " +
                    actor_id + " was not found"
                })
        except (DBAPIError, SQLAlchemyError):
            abort(500)
        return '', 204

    @api.doc('update a actor by id')
    @api.marshal_with(_actor)
    @requires_auth('update:actor')
    def patch(payload, self, actor_id):
        """
        update_actor: updates a actor given id
        Args:
            title (data type: str) optional 
            release_date (data type: str) optional
        Returns:
            returns success if the actor is updated
        """
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            updated_actor = (actor_service.
                             update_actor(actor_id, name, age, gender))
            if not updated_actor:
                raise NotFound({
                    "status": 404,
                    "description": "Actor with id " +
                    actor_id + " was not found"
                })
        except ValidationError as exc:
            raise BadRequest({
                "status": 400,
                "description": exc.error
            })
        return updated_actor.format(), 200


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
