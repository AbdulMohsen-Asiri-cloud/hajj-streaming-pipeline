import json
from kafka import KafkaConsumer
from datetime import datetime

consumer = KafkaConsumer(
    'hajj-weather',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

print("👂 Consumer شغال — يستقبل بيانات المشاعر لحظياً...\n")

for message in consumer:
    data = message.value

    # تحليل الحرارة
    if data['temp'] > 42:
        alert = "🔴 خطر شديد"
    elif data['temp'] > 38:
        alert = "🟡 تحذير"
    else:
        alert = "🟢 طبيعي"

    print(f"📍 {data['location']}")
    print(f"   🌡️  الحرارة  : {data['temp']}°C | يحس بـ {data['feels_like']}°C")
    print(f"   💧 الرطوبة  : {data['humidity']}%")
    print(f"   💨 الرياح   : {data['wind_speed']} م/ث")
    print(f"   📊 الحالة   : {alert}")
    print(f"   🕐 الوقت    : {data['timestamp']}")
    print("-" * 45)