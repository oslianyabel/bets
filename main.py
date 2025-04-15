import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

PROXY = {
    "http": "http://osliani.figueiras:Osliany801*@proxy.desoft.cu:3128",
    "https": "http://osliani.figueiras:Osliany801*@proxy.desoft.cu:3128",
}

API_KEY = os.getenv("ODDS_API_KEY")
host = "https://api.the-odds-api.com"
endpoint_get_sports = f"/v4/sports/?apiKey={API_KEY}"

SPORT = "soccer_uefa_champions_league"  # Clave de la Champions League
REGION = "eu"  # Región (eu, us, uk, etc.)
MARKETS = "h2h,spreads,totals,btts,draw_no_bet"  # Todos los mercados
BOOKMAKER = "bet365"  # Solo cuotas de Bet365

url = f"{host}/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGION}&markets={MARKETS}&bookmakers={BOOKMAKER}"

try:
    response = requests.get(url, proxies=PROXY, timeout=10)
    response.raise_for_status()  # Lanza error si hay problemas HTTP (4XX/5XX)

    data = response.json()
    print(type(data))
    print(json.dumps(data, indent=2))

except requests.exceptions.RequestException as exc:
    print("Error al conectar con el proxy o la API:", exc)
