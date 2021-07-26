import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question = {
            'question': 'What are the names of the 4 starter Pokemon?',
            'answer': 'Squirtle, Charmander, Pikachu, Bulasaur',
            'difficulty': 1,
            'category': '5'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])   

    def test_get_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_questions(self):
            res = self.client().delete('/questions/15')
            data = json.loads(res.data)

            question = Question.query.filter(Question.id == 15).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], 15)
            # self.assertTrue(data['total_questions'])
            # self.assertTrue(len(data['questions']))
            self.assertEqual(question, None)

    def search_question(self):
        res = self.client().post('questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_404_invalid_search(self):
        res = self.client().post('questions/search', json={"searchTerm": "beebop"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))


    def test_404_if_question_does_not_exist(self):
            res = self.client().delete('/questions/1000')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unprocessable')


    def test_get_category_questions(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_category_questions(self):
        response = self.client().get('/categories/a/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_quiz(self):
        quiz_round = {'previous_questions': [], 'quiz_category': {
            'type': 'Geography', 'id': 15}}
        response = self.client().post('/quizzes', json=quiz_round)
        data = json.loads(response.data)

        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_get_quiz(self):
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

