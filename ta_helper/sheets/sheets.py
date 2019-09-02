import os 
import json
import pprint
import _pickle as pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as f:
    CONFIG = json.load(f)

TOKENPATH = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'token.pkl')
CREDENTIALPATH = os.path.join(os.path.dirname(__file__), '..', 'credentials', 'credentials.json')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def list_all_sheets():
    print('Listing all sheets in the config file...')
    print('#'*30)
    
    sheets = CONFIG['GOOGLE']['SHEETS']
    for sheet in sheets:
        pprint.pprint(sheets[sheet])
        


def get_sheet(name='default'):
    sid = CONFIG['GOOGLE']['SHEETS'][name]['id']
    srange = CONFIG['GOOGLE']['SHEETS'][name]['name']

    service = _setup()
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sid,
                                range=srange).execute()
    
    values = result.get('values', [])
    
    header = values[0]
    values = values[1:]


    rtn = {
        'header': header,
        'value':values
        }
    
    return rtn


def _setup():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKENPATH):
        with open(TOKENPATH, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALPATH, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(TOKENPATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service




