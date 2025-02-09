import requests
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BINANCE_API_URL")

def get_crypto_price(symbol: str):
    url = f"{BASE_URL}?symbol={symbol.upper()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data["price"])
        return data["price"]
    else:
        return f"Error: {response.status_code}"