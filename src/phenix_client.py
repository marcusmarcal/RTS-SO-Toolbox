class PhenixRTS:
    def __init__(self, app_id: str, password: str):
        self.app_id = app_id
        self.password = password
        self.token = None

    def authenticate(self):
        # Simulate requesting a Bearer token using AppID and Password
        # In a real-world scenario, this would involve actual API calls.
        self.token = f"Bearer {self.app_id}:{self.password}"
        print(f"Authenticated with token: {self.token}")

    def get(self, url: str):
        if not self.token:
            raise Exception("Authentication required. Please call authenticate() first.")
        # Add code for GET request using self.token
        print(f"GET request to {url} with token {self.token}")

    def post(self, url: str, data: dict):
        if not self.token:
            raise Exception("Authentication required. Please call authenticate() first.")
        # Add code for POST request using self.token
        print(f"POST request to {url} with data {data} and token {self.token}")

    def put(self, url: str, data: dict):
        if not self.token:
            raise Exception("Authentication required. Please call authenticate() first.")
        # Add code for PUT request using self.token
        print(f"PUT request to {url} with data {data} and token {self.token}")

    def delete(self, url: str):
        if not self.token:
            raise Exception("Authentication required. Please call authenticate() first.")
        # Add code for DELETE request using self.token
        print(f"DELETE request to {url} with token {self.token}")
