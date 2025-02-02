import os
from datetime import datetime, timezone
from flask import Flask, render_template, request,Response
from dotenv import load_dotenv
import requests
from prometheus_client import Counter, Histogram, generate_latest

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests", ["endpoint"])
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Latency of requests in seconds", ["endpoint"]
)
city_search_count = Counter(
    "city_search_count", "Number of times each city has been looked at", ["city"]
)

app = Flask(__name__)
load_dotenv()

@app.route('/')
def index():
    REQUEST_COUNT.labels(endpoint="/").inc()
    with REQUEST_LATENCY.labels(endpoint="/").time():
        return render_template('index.html')

@app.route('/search', methods=['GET'])
def weather():
    REQUEST_COUNT.labels(endpoint="/search").inc()
    with REQUEST_LATENCY.labels(endpoint="/search").time():
        location = request.args.get('location')
        city_search_count.labels(city=location).inc()
        if not location:
            return render_template('index.html', error="Required: at least city or country.")
    api_key = os.getenv("API_KEY") 
    coordinates_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={api_key}"
    
    try:
        coordinates_response = requests.get(coordinates_url, timeout=5).json()
    except requests.exceptions.Timeout:
        return render_template('index.html', error="Request timed out. Please try again.")
    
    print(coordinates_response)
    print("API first call executed!")
    if len(coordinates_response) == 0:
        return render_template('index.html', error="Location not found. Please try again.")
    lat = coordinates_response[0]['lat']
    lon = coordinates_response[0]['lon']
    country = coordinates_response[0].get('state', 'Unknown')
    weather_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&units=metric&appid={api_key}"
    
    try:
        response = requests.get(weather_url, timeout=5).json()
    except requests.exceptions.Timeout:
        return render_template('index.html', error="Request timed out. Please try again!.")
    print(response)
    
    forecast = []
    for day in response.get('daily', [])[:7]:
        date = datetime.fromtimestamp(day['dt'], tz=timezone.utc).strftime('%-d/%-m/%Y')
        temp_day = day['temp']['day']
        temp_night = day['temp']['night']
        humidity = day['humidity']
        
        forecast.append({
            'date': date,
            'temp_day': temp_day,
            'temp_night': temp_night,
            'humidity': humidity
        })

    if location.casefold() == country.casefold():
        return render_template('weather.html', country=country, forecast=forecast)
    
    return render_template('weather.html', location=location, country=country, forecast=forecast)

@app.route("/metrics")
def metrics():
     return Response(generate_latest(), content_type="text/plain")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
