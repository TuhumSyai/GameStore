import requests

API_KEY = "2b27fe820d7a4aac84a82ad564f939f3"
BASE_URL = "https://api.rawg.io/api/"

def get_games():
    url = f"{BASE_URL}games?key={API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None













































