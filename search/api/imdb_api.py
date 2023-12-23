import requests

class IMDbAPI:
    def __init__(self, api_key):
        self.base_url = "https://imdb8.p.rapidapi.com/title/v2/find"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
        }

    def search_movies(self, query):
        response = self._make_request(self.base_url, query)
        return response.json()

    def get_movie_details(self, imdb_id):
        endpoint = f"{self.base_url}{imdb_id}"
        response = self._make_request(endpoint)

        try:
            response_json = response.json()
        except ValueError as e:
            # Handle the case where the response is not a valid JSON
            print(f"Error: Unable to parse API response as JSON. {e}")
            return None

        if 'error' in response_json:
            # Handle API error response
            error_message = response_json['error'].get('message', 'Unknown error')
            print(f"API Error: {error_message}")
            return None

        return response_json

    def _make_request(self, url, params=None):
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response
