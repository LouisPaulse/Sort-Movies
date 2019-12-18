import json
import requests


class OMBdApi:
    def __init__(self, api_key):
        self.api_url = f'http://www.omdbapi.com/?apikey={api_key}'

    def search_by_title(self, movie_title):
        movie_title = movie_title.replace(' ', '+')
        self.api_url = f'{self.api_url}&t={movie_title}'

        response = requests.post(self.api_url)

        response = json.loads(response.content.decode('utf-8'))
        return response
