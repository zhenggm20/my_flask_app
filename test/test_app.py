import unittest
from app import app, db, Task
from datetime import datetime
from flask import json

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_task(self):
        due_date = datetime.strptime("2024-09-15T10:00:00", '%Y-%m-%dT%H:%M:%S')
        response = self.app.post('/tasks', 
                                 content_type='application/json',
                                 data=json.dumps(dict(
                                     title="Test Task",
                                     description="This is a test.",
                                     due_date=due_date.isoformat()
                                 )),
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_tasks(self):
        self.test_add_task()
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        tasks = json.loads(response.data)
        self.assertGreater(len(tasks), 0)

if __name__ == "__main__":
    unittest.main()