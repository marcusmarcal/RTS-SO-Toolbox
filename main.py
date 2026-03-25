import requests
import base64
from urllib.parse import quote

class PhenixRTS:
    """
    PhenixRTS API client usando Basic Authentication.
    """

    def __init__(self, app_id: str, password: str, base_url: str = 'https://pcast.phenixrts.com'):
        self.app_id = app_id
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self):
        credentials = f"{self.app_id}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.session.headers.update({
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def authenticate(self):
        try:
            response = self.session.get(f'{self.base_url}/pcast/composition')
            if response.status_code == 200:
                print('✓ Authentication successful')
                return True
            else:
                print(f'✗ Authentication failed: {response.status_code}')
                return False
        except Exception as e:
            print(f'✗ Authentication error: {e}')
            return False

    def get_channels(self):
        """Retorna todos os canais da conta"""
        try:
            response = self.session.get(f'{self.base_url}/pcast/channels')
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "ok":
                return data.get("channels", [])
            else:
                raise RuntimeError(f"API returned status: {data.get('status')}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'Failed to get channels: {str(e)}')

    def get_publishers_count(self, channel_id: str):
        """
        Verifica a saúde de um canal (número de publishers).
        Endpoint: /pcast/channel/<urlEncodedChannelId>/publishers/count
        """
        encoded_id = quote(channel_id)
        endpoint = f'pcast/channel/{encoded_id}/publishers/count'

        try:
            response = self.session.get(f'{self.base_url}/{endpoint}')
            
            if response.status_code == 200:
                try:
                    return response.json()
                except:
                    # Algumas respostas retornam apenas o número como texto
                    return {"status": "ok", "count": int(response.text.strip()) if response.text.strip().isdigit() else 0}
            elif response.status_code == 412:
                return {"status": "fail", "count": 0, "message": "Fewer publishers than required"}
            else:
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'Health check failed for channel {channel_id}: {str(e)}')