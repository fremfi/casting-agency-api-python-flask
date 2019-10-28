import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app.main.controller import movie_controller

from app.main import create_app, db
from app.main.model.movie import Movie
from app import blueprint
import requests
import os


class MovieTestCase(unittest.TestCase):
    """This class represents the movie test case"""

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
        movie = Movie(
            title="Joker",
            release_date="2019-10-04"
        )
        movie.insert()

    def test_get_movies(self):
        res = self.client().get('/movies/', headers=self.auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_beyond_valid_movies_page(self):
        res = (self.client().get('/movies?page=1000',
               headers=self.auth_header,
               follow_redirects=True))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error']['status'], 404)

    def test_create_movie(self):
        new_movie = {
            "release_date": "2019-10-04",
            "title": "Test Movie"
        }
        res = (self.client().post('/movies/', json=new_movie,
               headers=self.auth_header))
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.title == new_movie["title"]).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['title'], new_movie["title"])

    def test_400_sent_if_posted_question_isnt_formatted_correctly(self):
        res = (self.client().post('/movies/', headers=self.auth_header,
               json={
                    "release_date": "2019-10-04",
                    "title": ""
                }))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], {
            "status": 400,
            "description": "title cannot be empty."
        })

    def test_update_movie(self):
        updated_movie = {
            "title": "New Test Movie"
        }
        res = (self.client().patch('/movies/1',
               headers=self.auth_header, json=updated_movie))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['title'], updated_movie["title"])

    def test_delete_movie(self):
        res = (self.client().delete('/movies/1',
               headers=self.auth_header))

        movie = Movie.query.filter(Movie._id == 1).one_or_none()

        self.assertEqual(res.status_code, 204)
        self.assertEqual(movie, None)

    def test_404_sent_if_question_being_deleted_does_not_exist(self):
        res = (self.client().delete('/movies/1000',
               headers=self.auth_header))

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
