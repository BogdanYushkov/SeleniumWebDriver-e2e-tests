import requests

BASE_URL = "http://localhost:3000"

class TracksAPIClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def get_projects(self):
        return requests.get(f"{self.base_url}/projects")

    def create_project(self, data):
        return requests.post(f"{self.base_url}/projects", json=data)

    def delete_project(self, project_id):
        return requests.delete(f"{self.base_url}/projects/{project_id}")
