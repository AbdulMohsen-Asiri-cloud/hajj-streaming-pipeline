import requests
import json
import time
from kafka import KafkaProducer
from datetime import datetime

API_KEY = "YOUR_OPENWEATHER_API_KEY"

POWER_BI_URL = "YOUR_POWER_BI_PUSH_URL"

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

CITIES = [
    {"name": "Mecca",     "lat": 21.3891, "lon": 39.8579},
    {"name": "Mina",      "lat": 21.4131, "lon": 39.8936},
    {"name": "Arafat",    "lat": 21.3547, "lon": 39.9845},
    {"name": "Muzdalifa", "lat": 21.3761, "lon": 39.9366},
]

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
)

def calculate_heat_index(temp, humidity):
    hi = (-8.78469475556 +
          1.61139411 * temp +
          2.33854883889 * humidity +
          -0.14611605 * temp * humidity +
          -0.012308094 * temp**2 +
          -0.0164248277778 * humidity**2 +
          0.002211732 * temp**2 * humidity +
          0.00072546 * temp * humidity**2 +
          -0.000003582 * temp**2 * humidity**2)
    return round(hi, 1)

def fetch_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": city["lat"],
        "lon": city["lon"],
        "appid": API_KEY,
        "units": "metric",
        "lang": "ar"
    }
    r = requests.get(url, params=params)
    data = r.json()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    heat_index = calculate_heat_index(temp, humidity)

    return {
        "timestamp": datetime.now().isoformat(),
        "location": city["name"],
        "temp": temp,
        "feels_like": data["main"]["feels_like"],
        "humidity": humidity,
        "wind_speed": data["wind"]["speed"],
        "heat_index": heat_index,
        "heat_alert": "⚫ خطر شديد - طوارئ فورية" if temp > 44 else "🔴 خطر - ضربة شمس محتملة" if temp > 40 else "🟡 تحذير - إجهاد حراري" if temp > 35 else "🟢 طبيعي"
    }

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    })

def push_to_powerbi(records):
    headers = {"Content-Type": "application/json"}
    r = requests.post(POWER_BI_URL, json=records, headers=headers)
    if r.status_code == 200:
        print("📊 Power BI ✅")
    else:
        print(f"📊 Power BI ❌ {r.status_code}")

print("🚀 Producer شغال — بيانات مشاعر الحج كل 5 دقائق...")

while True:
    records = []
    alerts = []

    for city in CITIES:
        try:
            record = fetch_weather(city)
            producer.send('hajj-weather', value=record)
            records.append(record)
            print(f"✅ {record['location']} | {record['temp']}°C | 🌡️ Heat Index: {record['heat_index']} | {record['heat_alert']}")

            if record['temp'] > 35:
                alerts.append(
                    f"📍 <b>{record['location']}</b>\n"
                    f"🌡️ الحرارة: {record['temp']}°C\n"
                    f"🔥 Heat Index: {record['heat_index']}°C\n"
                    f"💧 الرطوبة: {record['humidity']}%\n"
                    f"⚠️ الحالة: {record['heat_alert']}"
                )
        except Exception as e:
            print(f"❌ خطأ: {e}")

    push_to_powerbi(records)

    if alerts:
        message = "🚨 <b>تنبيه مشاعر الحج</b>\n\n" + "\n\n".join(alerts)
        send_telegram(message)
        print("📱 Telegram ✅")

    print("--- انتظر 5 دقائق ---")
    time.sleep(60
    )