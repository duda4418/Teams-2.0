from tkinter import messagebox

import requests

class Client:
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }
    def get(self, endpoint ):
        response = requests.get(endpoint, headers=self.headers)
        succes = self._check_response(response)
        if succes:
            return response.json()
        return None

    def post(self, endpoint, body):
        response = requests.post(endpoint, headers = self.headers, json = body)
        succes = self._check_response(response)
        if succes:
            return response.json()
        return None

    def delete(self, endpoint):
        response = requests.delete(endpoint, headers = self.headers)
        succes = self._check_response(response)
        if succes:
            return response.json()
        return None
    @staticmethod
    def _check_response(response):
        success = response.ok
        if not success:
            messagebox.showerror("API error message", response.content)
        return success