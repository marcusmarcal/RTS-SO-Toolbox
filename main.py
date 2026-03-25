"""
RTS-SO-Toolbox - Main entry point for the application
This is the main entry point for the RTS-SO-Toolbox application.
"""

from src.config import get_env_variable
from src.phenix_client import PhenixRTS
from src.stream_monitor import StreamMonitor

if __name__ == '__main__':
    print('RTS-SO-Toolbox is running...')
    
    # Load configuration from environment variables
    try:
        api_key = get_env_variable('PHENIXRTS_API_KEY')
        api_secret = get_env_variable('PHENIXRTS_API_SECRET')
        print(f'API Key loaded successfully')
    except RuntimeError as e:
        print(f'Error loading configuration: {e}')