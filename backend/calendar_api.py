import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError


app = Flask(__name__)

@app.route("/oauth2callback", methods=["GET"])
def oauth2callback():
    code = request.args.get("code") 

