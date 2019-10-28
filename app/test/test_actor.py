import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app.main.controller import actor_controller

from app.main import create_app, db
from app.main.model.actor import Actor
from app import blueprint
import http.client
import requests
import os


class ActorTestCase(unittest.TestCase):
    """This class represents the actor test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('testing')
        self.app.register_blueprint(blueprint)
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()
            db.session.commit()
            self.populate_db()

        AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
        res = (requests.post(url='https://' + AUTH0_DOMAIN + '/oauth/token',
               data={
                    "grant_type": "client_credentials",
                    "client_id": "uqxA7Rj5RK1BcZ4edFpdNoxAy9VNq8vS",
                    "client_secret": "vmYihu3sQ-XC4jCCI19VTmUGxvfDNF-mgjS_XrdmBGcpKvnT1L4gw2hZXAOOIZrm",  # nopep8
                    "audience": "castingagencyauth"
                }))
        access_token = res.json()['access_token']
        self.auth_header = {'Authorization': 'Bearer ' + access_token}

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def populate_db(self):
        actor = Actor(
            name="Dwayne Johnson",
            age=30,
            gender="MALE"
        )
        actor.insert()

    def test_create_actor(self):
        new_actor = {
            "name": "Rainbow Johnson",
            "age": 28,
            "gender": "FEMALE"
        }
        res = (self.client().post('/actors/', json=new_actor,
               headers=self.auth_header))
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.name == new_actor["name"]).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['name'], new_actor["name"])

    def test_400_sent_if_posted_question_isnt_formatted_correctly(self):
        res = (self.client().post('/actors/', headers=self.auth_header,
               json={
                    "name": "Rainbow Johnson",
                    "age": 28,
                    "gender": "RANDOM"
                }))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], {
            "status": 400,
            "description": "gender is either MALE or FEMALE"
        })

    def test_get_actors(self):
        res = self.client().get('/actors/', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_beyond_valid_actors_page(self):
        res = (self.client().get('/actors?page=1000',
               headers=self.auth_header,
               follow_redirects=True))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error']['status'], 404)

    def test_update_actor(self):
        updated_actor = {
            "name": "Nancy Johnson",
            "gender": "FEMALE"
        }

        res = (self.client().patch('/actors/1',
               headers=self.auth_header, json=updated_actor))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['age'], 30)
        self.assertEqual(data['gender'], updated_actor["gender"])
        self.assertEqual(data['name'], updated_actor["name"])

    def test_delete_actor(self):
        res = (self.client().delete('/actors/1',
               headers=self.auth_header))

        actor = Actor.query.filter(Actor._id == 1).one_or_none()

        self.assertEqual(res.status_code, 204)
        self.assertEqual(actor, None)

    def test_404_sent_if_question_being_deleted_does_not_exist(self):
        res = (self.client().delete('/actors/1000',
               headers=self.auth_header))

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
