import unittest
import base64
import json

from flask import Flask, g
from app import app
from db import init_db, destroy_db

from models import User


class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        self.app = app.test_client()
        init_db()
        self.user = User(email='test', password='test')
        self.user.save()

    def tearDown(self):
        destroy_db()

    def open_with_auth(self, url, method, username, password, json=None):
        return self.app.open(url,
            method=method,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" \
                    + password, 'ascii')).decode('ascii')
            }, 
            json=json
        )

    def test_create_user(self):
        res = self.app.post('/user/create/', json={'email': 'test1', 'password': 'test1'})
        self.assertEqual(res.status_code, 201)

    def test_get_todo_list(self):
        res = self.open_with_auth('/todo/create/', 'POST', 'test', 'test', json={'text': 'test item1', 'due_date': '2020-10-23T08:00:00-07:00'})
        res = self.open_with_auth('/todo/create/', 'POST', 'test', 'test', json={'text': 'test item1', 'due_date': '2010-10-23T08:00:00-07:00'})
        
        res = self.open_with_auth('/todo/', 'GET', 'test', 'test')
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['results']), 2)
        self.assertEqual(json_data['results'][0]['id'], 1)

        res = self.open_with_auth('/todo/?sort=true', 'GET', 'test', 'test')
        self.assertEqual(res.status_code, 200)
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['results']), 2)
        self.assertEqual(json_data['results'][0]['id'], 2)

    def test_create_item(self):
        res = self.open_with_auth('/todo/create/', 'POST', 'test', 'test', json={'text': 'test item1'})
        self.assertEqual(res.status_code, 201)

    def test_complete_item(self):
        res = self.open_with_auth('/todo/create/', 'POST', 'test', 'test', json={'text': 'test item1'})
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(json_data['is_completed'], False)

        res = self.open_with_auth('/todo/{}/complete/'.format(json_data['id']), 'PATCH', 'test', 'test')
        json_data = json.loads(res.data)
        self.assertEqual(json_data['is_completed'], True)

    def test_view_hidden_items(self):
        res = self.open_with_auth('/todo/create/', 'POST', 'test', 'test', json={'text': 'test item1'})
        res = self.open_with_auth('/todo/create/', 'POST', 'test', 'test', json={'text': 'test item1'})
        self.assertEqual(res.status_code, 201)
        
        json_data = json.loads(res.data)
        res = self.open_with_auth('/todo/{}/complete/'.format(json_data['id']), 'PATCH', 'test', 'test')
        
        res = self.open_with_auth('/todo/?show_completed=true', 'GET', 'test', 'test')
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['results']), 2)
       
        res = self.open_with_auth('/todo/', 'GET', 'test', 'test')
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['results']), 1)

    def test_delete_item(self):
        res = self.open_with_auth('/todo/create/', 'POST', 'test', 'test', json={'text': 'test item1'})
        json_data = json.loads(res.data)
        
        res = self.open_with_auth('/todo/{}/delete/'.format(json_data['id']), 'DELETE', 'test', 'test')
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.open_with_auth('/todo/', 'GET', 'test', 'test')
        json_data = json.loads(res.data)
        self.assertEqual(len(json_data['results']), 0)

if __name__ == '__main__':
    unittest.main()
