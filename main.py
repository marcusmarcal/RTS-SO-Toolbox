import os
from dotenv import load_dotenv

load_dotenv()

app_id = os.getenv('PHENIXRTS_APP_ID')
password = os.getenv('PHENIXRTS_PASSWORD')

# Add code to initialize PhenixRTS client with app_id and password
# client = PhenixRTS(app_id=app_id, password=password)