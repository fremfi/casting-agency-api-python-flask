from flask_restplus import Api
from flask import Blueprint

from .main.controller.movie_controller import api as movie_ns
from .main.controller.actor_controller import api as actor_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='CASTING AGENCY API',
          version='1.0',
          )

api.add_namespace(movie_ns, path='/movies')
api.add_namespace(actor_ns, path='/actors')
