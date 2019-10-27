import datetime

from app.main import db
from app.main.model.actor import Actor


def get_actors(page, per_page):
    return (Actor.query.order_by(Actor._name.desc()).
            paginate(page, per_page, error_out=False))


def get_actor(actor_id):
    return Actor.query.get(actor_id)


def post_actor(name, age, gender):
    actor = Actor(
        name=name,
        age=age,
        gender=gender,
    )
    actor.insert()
    return actor


def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        actor.delete()
    return actor


def update_actor(actor_id, name, age, gender):
    actor = Actor.query.get(actor_id)
    if actor:
        actor.name = name or actor.name
        actor.age = age or actor.age
        actor.gender = gender or actor.gender.name
        actor.update()

    return actor
