class PhenixRTS:
    """
    PhenixRTS API client for making requests to the PhenixRTS service.
    """

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params=None):
        import requests
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(f'{self.base_url}/{endpoint}', headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        import requests
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        response = requests.post(f'{self.base_url}/{endpoint}', headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None):
        import requests
        headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
        response = requests.put(f'{self.base_url}/{endpoint}', headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        import requests
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.delete(f'{self.base_url}/{endpoint}', headers=headers)
        response.raise_for_status()
        return response.status_code
