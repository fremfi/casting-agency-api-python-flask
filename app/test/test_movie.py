import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app.main.controller import movie_controller

from app.main import create_app
from app.main.model.movie import Movie
from app import blueprint


class MovieTestCase(unittest.TestCase):
    """This class represents the movie test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test')
        self.app.register_blueprint(blueprint)
        self.client = self.app.test_client
        # Executive Director Role Token
        self.exec_dir_headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1qWTNOalV4TnpCRE1FWXpRalJEUTBRelF6VkRSVGMwUWpNM1F6aEVRak01TnpBM1JqVXpRdyJ9.eyJpc3MiOiJodHRwczovL2ZyZW1maS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRiNGM0NjBlOWMwNzQwZDYxMzczYWQ5IiwiYXVkIjoiY2FzdGluZ2FnZW5jeWF1dGgiLCJpYXQiOjE1NzIxOTQ4OTMsImV4cCI6MTU3MjIwMjA5MywiYXpwIjoiVXhOdml5Yjh0eUhlaDFkSTBYc2syOWp6MDZkUUVUZWEiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvciIsImNyZWF0ZTptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidXBkYXRlOmFjdG9yIiwidXBkYXRlOm1vdmllIl19.jix7dg9B4zjTOFe4NIupkVxAHTWVdGObQvwLgidLeQBp2A08I4sLjEj6bo7nSEmQy-4L10QiTvTHvNCcY0KIkPVk6Amjhsu5XgnM3mKJma2jRYEuRefnxBei8qg0jNaR5xCHsfbvcZFQ69k99AkP-6qwMZ1hszKvXTaLunsssG13Y-QojTLSSvDAY6gNN4VP9NI-SqO_DXoo_pete3Qo6FbunlLuJAJnYnBpVKUwwOcHacO3b0lYOEHHMlyxfz23_tu4Z-gWH5mrUEdBA_8f7zYlFY1YKbAaFlv8vGXjWTFGYxpRLqwSkZicdBn7dSJmyQrpmZtea3LngOlNamdOaA'}  # nopep8

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def test_get_movies(self):
        res = self.client().get('/movies/', headers=self.exec_dir_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_404_sent_requesting_beyond_valid_movies_page(self):
        res = (self.client().get('/movies?page=1000',
               headers=self.exec_dir_headers,
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
               headers=self.exec_dir_headers))
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.title == new_movie["title"]).first()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['title'], new_movie["title"])

    def test_400_sent_if_posted_question_isnt_formatted_correctly(self):
        res = (self.client().post('/movies/', headers=self.exec_dir_headers,
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
               headers=self.exec_dir_headers, json=updated_movie))
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie._id == 1).first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(movie.title, updated_movie["title"])
        self.assertEqual(data['title'], updated_movie["title"])

    def test_delete_movie(self):
        res = (self.client().delete('/movies/2',
               headers=self.exec_dir_headers))

        movie = Movie.query.filter(Movie._id == 2).one_or_none()

        self.assertEqual(res.status_code, 204)
        self.assertEqual(movie, None)

    def test_404_sent_if_question_being_deleted_does_not_exist(self):
        res = (self.client().delete('/movies/1000',
               headers=self.exec_dir_headers))

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
