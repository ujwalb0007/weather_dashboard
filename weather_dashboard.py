import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("cod") != "200":
        print("❌ Error:", data.get("message"))
        return None

    forecast = []
    for entry in data["list"]:
        dt = datetime.fromtimestamp(entry["dt"])
        temp = entry["main"]["temp"]
        desc = entry["weather"][0]["description"]
        forecast.append({"Date": dt, "Temp (°C)": temp, "Description": desc})

    df = pd.DataFrame(forecast)
    return df

def show_chart(df, city):
    plt.figure(figsize=(10, 4))
    plt.plot(df["Date"], df["Temp (°C)"], marker="o")
    plt.title(f"7-Day Temperature Trend - {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def save_csv(df, city):
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{city}_forecast.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ Data saved to {file_path}")

def main():
    print("🌦️ LIVE WEATHER DASHBOARD 🌦️")
    city = input("Enter city name: ").strip()

    df = get_weather(city)
    if df is not None:
        print(df.head())
        show_chart(df, city)
        save_csv(df, city)

if __name__ == "__main__":
    main()
