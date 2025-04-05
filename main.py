from flask import Flask, request, jsonify
import requests
import pickle
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from googletrans import Translator
import google.generativeai as genai
from flask_cors import CORS
from PIL import Image
import io
import gdown
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

GEN_API_KEY = os.getenv("GEN_API_KEY")  
API_KEY = os.getenv("API_KEY") 

if not GEN_API_KEY or not API_KEY:
    raise ValueError("API keys not found! Set GENAI_API_KEY and WEATHER_API_KEY.")

genai.configure(api_key=GEN_API_KEY)

# Weather API Route
@app.route('/weather', methods=['POST'])
def get_weather_data():
    city = request.json
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}"
    weather_data = requests.get(url).json()

    if 'error' in weather_data:
        return jsonify({'error': 'Unable to fetch weather data'}), 400

    current_temp = weather_data['current']['temp_c']
    humidity = weather_data['current']['humidity']
    wind_speed = weather_data['current']['wind_kph']
    rain_chance = weather_data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
    forecast_text = weather_data['forecast']['forecastday'][0]['day']['condition']['text']

    weather_summary = {
        "Current Weather in": city,
        "temperature": f"{current_temp}°C",
        "humidity": f"{humidity}%",
        "windSpeed": f"{wind_speed} km/h",
        "rainChance": f"{rain_chance}%",
        "forecast": forecast_text
    }
    return jsonify(weather_summary)

# Farming Insights Route
@app.route('/farming-insights', methods=['POST'])
def get_farming_insights():
    data = request.json
    city = data.get('city', '')
    weather_summary = data.get('weather_summary', '')
    language = data.get('language', 'English')

    prompt = f"""
    Analyze this weather data for {city} and provide farming-specific insights in {language}:
    1. Best farming practices based on temperature, humidity, and rainfall.
    2. Irrigation techniques for optimal water use.
    3. Pest and disease risks under these conditions.
    4. Weather-related farming risks such as drought or heat stress.

    Weather Data:
    {weather_summary}
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([prompt])

    return jsonify({"farming_insights": response.text})

# Crop Image Analysis Route
@app.route('/analyze-crop', methods=['POST'])
def analyze_crop():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        image_file = request.files['image']
        language = request.form.get("language", "English")

        image = Image.open(image_file)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="JPEG")

        model = genai.GenerativeModel("gemini-2.0-flash")
        ai_response = model.generate_content([
            image,
            f"Analyze this crop image and detect any diseases. Provide recommendations in {language}."
        ])

        return jsonify({"analysis": ai_response.text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Download Model from Google Drive
file_id = "1aBcDeFgHiJKlmNOPqRS"  
output_path = "model.pkl"

def download_model():
    if not os.path.exists(output_path):
        url = "https://drive.google.com/file/d/1eq7QG9PiO1w8aVfdhbe4U0erYzJUorwe/view?usp=sharing"
        gdown.download(url=url, output=output_path, fuzzy=True)

download_model()

# Load Model
model = None

def load_model():
    global model
    if model is None:
        try:
            with open(output_path, "rb") as f:
                model = pickle.load(f)
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")

load_model()

# Price Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        day_of_year = int(data['dayOfYear'])
        min_price = float(data['minPrice'])
        max_price = float(data['maxPrice'])

        input_data = pd.DataFrame({
            'DayOfYear': [day_of_year],
            'Min Price': [min_price],
            'Max Price': [max_price]
        })

        prediction = model.predict(input_data)[0]
        return jsonify({'predictedPrice': round(prediction, 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Translator
translator = Translator()

def translate_to_english(text):
    try:
        detected_lang = translator.detect(text).lang
        if detected_lang != 'en':
            return translator.translate(text, dest='en').text, detected_lang
        return text, 'en'
    except Exception:
        return text, 'en'

def translate_from_english(text, target_lang):
    try:
        if target_lang != 'en':
            return translator.translate(text, dest=target_lang).text
        return text
    except Exception:
        return text

# AI Chat Route
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "")

        translated_input, detected_lang = translate_to_english(user_input)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(translated_input)

        translated_response = translate_from_english(response.text, detected_lang)
        return jsonify({"response": translated_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# AI Weather Prediction
def get_weather_prediction(city):
    prompt = f"Predict the weather for {city} for the next 3 days."
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip() if response and response.text else "No weather data available."

# AI Weather Prediction Route
@app.route('/predict-weather', methods=['POST'])
def predict_weather():
    data = request.json
    city = data.get('city', '')

    if not city:
        return jsonify({"error": "City name is required"}), 400

    prediction = get_weather_prediction(city)
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
