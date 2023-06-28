from requests.auth import HTTPBasicAuth
import os

TEQUILA_API_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_API_KEY = "QdDEcBPW2QCiEpB3AZEq7VPbIkXApvPh"
TEQUILA_HEADERS = {
    "apikey": "Lge-77DB1Z-5NLgeMU7Z7EFWa3pWwnCW"
}
SHEETY_USERNAME = "martinpytesting00172"
SHEETY_PASSWORD = "bcq5870469c8476bcfysbg7487gwreh"
SHEETY_BASIC_AUTH = HTTPBasicAuth(SHEETY_USERNAME, SHEETY_PASSWORD)
SHEETY_API = "https://api.sheety.co/644141880195acc45d63b69d2f8c6c7b/myFlightSearch/sheet1"

GMAIL_USERNAME = "martin.py.testing@gmail.com"
GMAIL_SECURITY_CODE = os.environ.get("GMAIL_SECURITY_CODE")

