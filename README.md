# 🕌 Hajj Weather Live Streaming Pipeline

Real-time weather monitoring system for Hajj holy sites using Apache Kafka, Python, Power BI, and Telegram alerts.

---

## 📌 Overview

This project monitors real-time weather conditions across the four holy sites of Hajj (Mecca, Mina, Arafat, Muzdalifa) and sends instant alerts to field supervisors via Telegram when dangerous heat conditions are detected.

---

## 🏗️ Architecture

    OpenWeather API → Kafka → Consumer → Power BI Live Dashboard
                                       → Telegram Bot Alerts

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| Apache Kafka | Real-time data streaming queue |
| Docker | Running Kafka & Zookeeper |
| Python | Producer & Consumer scripts |
| OpenWeatherMap API | Live weather data source |
| Power BI Service | Real-time dashboard |
| Telegram Bot | Instant field alerts |

---

## 📁 Project Structure

    hajj-streaming/
    ├── docker-compose.yml   ← Kafka & Zookeeper setup
    ├── producer.py          ← Fetches weather & pushes to Kafka + Power BI
    ├── consumer.py          ← Receives & analyzes streaming data
    └── README.md

---

## 🚀 Getting Started

### Requirements
- Docker Desktop
- Python 3.10+
- OpenWeatherMap API key (free)
- Power BI Service account
- Telegram Bot token

### Install dependencies

    pip install kafka-python requests

### Run Kafka

    docker-compose up -d

### Run Producer

    python producer.py

### Run Consumer

    python consumer.py

---

## 🌡️ Heat Alert Levels

Based on Saudi Ministry of Health guidelines:

| Level | Temperature | Action |
|---|---|---|
| 🟢 Normal | Below 35°C | Regular monitoring |
| 🟡 Warning | 35 - 40°C | Alert supervisors |
| 🔴 Danger | 40 - 44°C | Immediate action |
| ⚫ Critical | Above 44°C | Emergency response |

---

## 📊 Power BI Dashboard

Live dashboard showing:
- 🌡️ Temperature per site (Card)
- 💧 Humidity (Card)
- 💨 Wind Speed (Card)
- 🔥 Heat Index (Card)
- 📊 Temperature comparison across sites (Bar Chart)
- 📈 Temperature over time (Line Chart)

---

## 📱 Telegram Alerts

Bot sends instant alerts when temperature exceeds 35°C with location, temperature, heat index, humidity, and danger level.

---

## 🔮 Future Development

- [ ] Add crowd density data
- [ ] Auto PDF reports for management
- [ ] GPS pilgrim tracking
- [ ] Deploy on Azure cloud
- [ ] PySpark for big data processing

---

## 👨‍💻 Built in one day as a practical project for Hajj Data Analyst role


## 📸 Dashboard Screenshot
<img width="1374" height="480" alt="image" src="https://github.com/user-attachments/assets/7630776e-5d26-4886-b2f5-2b412a0f8508" />
