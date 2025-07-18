# tests/test_app.py

import unittest
import os
os.environ["TESTING"] = "true"

from app import create_app, initialize_db

from app import create_app

app = create_app()
initialize_db()

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        print("HTML CONTENT:\n", html)  # 👈 add this to inspect
        assert "<title>Affiq&#39;s Portfolio</title>" in html



    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert json["timeline_posts"] == []
        # TODO: Add more GET/POST route tests

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com",
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world, I'm John!"
        })
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

    def test_timeline_post(self):
        # Valid POST
        response = self.client.post("/api/timeline_post", data={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "content": "Hello from Jane!"
        })
        assert response.status_code == 200
        json = response.get_json()
        assert json["name"] == "Jane Doe"
        assert json["email"] == "jane@example.com"
        assert json["content"] == "Hello from Jane!"

        # Now do a GET to confirm it was added
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["timeline_posts"]) == 1
        assert data["timeline_posts"][0]["name"] == "Jane Doe"
