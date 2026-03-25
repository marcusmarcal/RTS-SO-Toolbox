import requests
import base64
from urllib.parse import quote

class PhenixRTS:
    """
    PhenixRTS API client for making authenticated requests to the PhenixRTS service.
    Uses Basic Authentication with AppID and Password (secret).
    """

    def __init__(self, app_id: str, password: str, base_url: str = 'https://pcast.phenixrts.com'):
        self.app_id = app_id
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self):
        """Setup Basic Authentication headers"""
        credentials = f"{self.app_id}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.session.headers.update({
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def authenticate(self):
        """Test authentication by making a simple GET request"""
        try:
            response = self.session.get(f'{self.base_url}/pcast/composition')
            if response.status_code == 200:
                print('✓ Authentication successful - API responded with 200 OK')
                return True
            elif response.status_code == 401:
                print('✗ Authentication failed - Invalid credentials (401 Unauthorized)')
                return False
            else:
                print(f'✗ API returned status code: {response.status_code}')
                print(f'Response: {response.text}')
                return False
        except requests.exceptions.RequestException as e:
            print(f'✗ Authentication error: {str(e)}')
            return False

    def get(self, endpoint: str, params=None):
        """Make GET request to PhenixRTS API"""
        try:
            response = self.session.get(
                f'{self.base_url}/{endpoint}', 
                params=params
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'GET request failed: {str(e)}')

    def post(self, endpoint: str, data=None):
        """Make POST request to PhenixRTS API"""
        try:
            response = self.session.post(
                f'{self.base_url}/{endpoint}', 
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'POST request failed: {str(e)}')

    def put(self, endpoint: str, data=None):
        """Make PUT request to PhenixRTS API"""
        try:
            response = self.session.put(
                f'{self.base_url}/{endpoint}', 
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'PUT request failed: {str(e)}')

    def delete(self, endpoint: str):
        """Make DELETE request to PhenixRTS API"""
        try:
            response = self.session.delete(f'{self.base_url}/{endpoint}')
            response.raise_for_status()
            return response.status_code
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'DELETE request failed: {str(e)}')

    # ==================== NOVO MÉTODO PARA SAÚDE DOS CANAIS ====================
    def get_publishers_count(self, channel_id: str, fail_if_less: int = None, with_streams: int = None, with_screen_name: str = None):
        """
        Verifica a saúde de um canal (número de publishers/ingests).
        Endpoint oficial: /pcast/channel/<urlEncodedChannelId>/publishers/count
        """
        encoded_id = quote(channel_id)
        endpoint = f'pcast/channel/{encoded_id}/publishers/count'

        params = {}
        if fail_if_less is not None:
            params['failIfLess'] = fail_if_less
        if with_streams is not None:
            params['withStreams'] = with_streams
        if with_screen_name:
            params['withScreenName'] = with_screen_name

        try:
            response = self.session.get(f'{self.base_url}/{endpoint}', params=params)

            if response.status_code == 200:
                try:
                    return response.json()
                except:
                    # Algumas respostas retornam apenas o número
                    return {"status": "ok", "count": response.text.strip()}
            elif response.status_code == 412:
                return {"status": "fail", "message": "Fewer publishers than required", "http_status": 412}
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'Health check failed for channel {channel_id}: {str(e)}')