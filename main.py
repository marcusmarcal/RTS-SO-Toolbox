import requests
import base64
from urllib.parse import quote

class PhenixRTS:
    """
    PhenixRTS API client using Basic Authentication.
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

    def get_channels(self):
        """Return all channels from the account"""
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
        Check number of publishers (ingests/sources) for a channel.
        Returns an integer (0 or more).
        """
        encoded_id = quote(channel_id)
        endpoint = f'pcast/channel/{encoded_id}/publishers/count'

        try:
            response = self.session.get(f'{self.base_url}/{endpoint}')
            
            if response.status_code == 200:
                text = response.text.strip()
                try:
                    return int(text)
                except ValueError:
                    return 0
            elif response.status_code == 412:
                return 0
            else:
                response.raise_for_status()
                return 0
        except Exception as e:
            raise RuntimeError(f'Health check failed for {channel_id}: {str(e)}')