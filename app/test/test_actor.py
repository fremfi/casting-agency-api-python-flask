import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app.main.controller import actor_controller

from app.main import create_app
from app.main.model.actor import Actor
from app import blueprint


class ActorTestCase(unittest.TestCase):
    """This class represents the actor test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test')
        self.app.register_blueprint(blueprint)
        self.client = self.app.test_client
        # Executive Director Role Token
        self.exec_dir_headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qWTNOalV4TnpCRE1FWXpRalJEUTBRelF6VkRSVGMwUWpNM1F6aEVRak01TnpBM1JqVXpRdyJ9.eyJpc3MiOiJodHRwczovL2ZyZW1maS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRiNGM0NjBlOWMwNzQwZDYxMzczYWQ5IiwiYXVkIjoiY2FzdGluZ2FnZW5jeWF1dGgiLCJpYXQiOjE1NzIxMzk3ODgsImV4cCI6MTU3MjE0Njk4OCwiYXpwIjoiVXhOdml5Yjh0eUhlaDFkSTBYc2syOWp6MDZkUUVUZWEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvciIsImNyZWF0ZTptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidXBkYXRlOmFjdG9yIiwidXBkYXRlOm1vdmllIl19.n8GfKFCdoRtW_APE2d-8M6RtanNHFL465-gRAMqSFtKr5dlB1GiEsbVtmoiU84lsm5DgDnbg49_ITWjv7Z-ntk-if5ehv1Zg0QivOF4bpOpl_a19mmB77c_3uqNF54sJM5G6f6uK5Q6Hw9fv_Qb7HBwUochcAMirvdnjdBSRbUxHDS90V1MzpyuSn568NNt56iNvWUbNcX1UqB8UEAFfgwUWTpOF_gQed0lRWRXAtMQeFiQiCiX4qWReqCpAj4XXD6ia7h-h-7BpbxV5vuAnAhwj3HxbG9IQiFNurtneaskIm9eoWg-fmqClr6I9OUMFFlrFqlpbq0B8FPpI5Za74A'}

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def test_get_actors(self):
        res = self.client().get('/actors/', headers=self.exec_dir_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_404_sent_requesting_beyond_valid_actors_page(self):
        res = (self.client().get('/actors?page=1000',
               headers=self.exec_dir_headers,
               follow_redirects=True))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error']['status'], 404)

    def test_create_actor(self):
        new_actor = {
            "name": "Rainbow Johnson",
            "age": 28,
            "gender": "FEMALE"
        }
        res = (self.client().post('/actors/', json=new_actor,
               headers=self.exec_dir_headers))
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.name == new_actor["name"]).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['name'], new_actor["name"])

    def test_400_sent_if_posted_question_isnt_formatted_correctly(self):
        res = (self.client().post('/actors/', headers=self.exec_dir_headers,
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

    def test_update_actor(self):
        updated_actor = {
            "name": "Nancy Johnson"
        }
        res = (self.client().patch('/actors/1',
               headers=self.exec_dir_headers, json=updated_actor))
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor._id == 1).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(actor.name, updated_actor["name"])
        self.assertEqual(data['name'], updated_actor["name"])

    # def test_delete_actor(self):
    #     res = (self.client().delete('/actors/42',
    #            headers=self.exec_dir_headers))

    #     actor = Actor.query.filter(Actor._id == 42).one_or_none()

    #     self.assertEqual(res.status_code, 204)
    #     self.assertEqual(actor, None)

    # def test_404_sent_if_question_being_deleted_does_not_exist(self):
    #     res = (self.client().delete('/actors/1000',
    #            headers=self.exec_dir_headers))

    #     self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
