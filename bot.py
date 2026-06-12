import time
import requests
from datetime import datetime

TELEGRAM_TOKEN = "8142613258:AAEuvhv7LgvFbsXgsKZzzYrjxJWrpPsi8YQ"
CHAT_ID = 1923391645

def send_telegram(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"✅ Отправлено")
    except Exception as e:
        print(f"Ошибка: {e}")

def get_funding(symbol):
    data = requests.get(f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={symbol}").json()
    return float(data['result']['list'][0]['fundingRate']) * 100

def get_basis(symbol):
    future = requests.get(f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={symbol}").json()
    spot = requests.get(f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}").json()
    f_price = float(future['result']['list'][0]['lastPrice'])
    s_price = float(spot['result']['list'][0]['lastPrice'])
    return ((f_price - s_price) / s_price) * 100

send_telegram("✅ Бот запущен на Render!")

while True:
    for symbol in ["BTCUSDT", "ETHUSDT", "SOLUSDT"]:
        try:
            funding = get_funding(symbol)
            basis = get_basis(symbol)
            print(f"{datetime.now().strftime('%H:%M:%S')} {symbol}: {funding:.3f}% / {basis:.2f}%")
            
            if (symbol == "BTCUSDT" and funding >= 0.02 and basis >= 0.08) or \
               (symbol == "ETHUSDT" and funding >= 0.03 and basis >= 0.10) or \
               (symbol == "SOLUSDT" and funding >= 0.04 and basis >= 0.15):
                send_telegram(f"🚨 СИГНАЛ {symbol}!\nФандинг: {funding:.3f}%\nБазис: {basis:.2f}%")
                time.sleep(60)
        except Exception as e:
            print(f"Ошибка {symbol}: {e}")
    
    time.sleep(300)
