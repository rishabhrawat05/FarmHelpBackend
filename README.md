# FarmHelp Backend

FarmHelp is a web-based platform designed to empower farmers with real-time, personalized, and localized farming support. The backend of FarmHelp is built using Python and Flask, providing various APIs to deliver agricultural expertise and support to farmers.

## Features

The FarmHelp backend includes the following features:

1. **Weather Data API**
   - Retrieves weather data for a specific city and provides a summary including temperature, humidity, wind speed, rain chance, and forecast.

2. **Farming Insights API**
   - Analyzes weather data and provides farming-specific insights such as best farming practices, irrigation techniques, pest and disease risks, and weather-related farming risks.

3. **Crop Image Analysis API**
   - Analyzes uploaded crop images to detect diseases and provides treatment recommendations using AI.

4. **Price Prediction API**
   - Predicts crop prices based on input data such as day of the year, minimum price, and maximum price.

5. **AI Chat API**
   - A chatbot that answers farming queries and provides guidance in real-time.

6. **Weather Prediction API**
   - Predicts weather for a specific city for the next three days using AI.

## Installation

To set up the FarmHelp backend locally, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/rishabhrawat05/FarmHelpBackend.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd FarmHelpBackend
    ```

3. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate    # On Windows use `venv\Scripts\activate`
    ```

4. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**

    Create a `.env` file in the project root and add the following environment variables:

    ```
    GEN_API_KEY=your_genai_api_key
    API_KEY=your_weather_api_key
    ```

6. **Download the machine learning model:**

    The model is downloaded automatically when the application is started.

## Usage

To run the FarmHelp backend, use the following command:

```bash
python main.py
```

The backend will be available at `http://0.0.0.0:5000`.

## API Endpoints

1. **Weather Data API**
    - Endpoint: `/weather`
    - Method: `POST`
    - Payload: `{ "city": "city_name" }`
    - Response: Weather summary for the specified city.

2. **Farming Insights API**
    - Endpoint: `/farming-insights`
    - Method: `POST`
    - Payload: `{ "city": "city_name", "weather_summary": "summary", "language": "language" }`
    - Response: Farming-specific insights based on the weather data.

3. **Crop Image Analysis API**
    - Endpoint: `/analyze-crop`
    - Method: `POST`
    - Payload: Image file and `language` in form data.
    - Response: Disease analysis and treatment recommendations for the uploaded crop image.

4. **Price Prediction API**
    - Endpoint: `/predict`
    - Method: `POST`
    - Payload: `{ "dayOfYear": int, "minPrice": float, "maxPrice": float }`
    - Response: Predicted crop price.

5. **AI Chat API**
    - Endpoint: `/chat`
    - Method: `POST`
    - Payload: `{ "message": "user_message" }`
    - Response: Response from the chatbot.

6. **Weather Prediction API**
    - Endpoint: `/predict-weather`
    - Method: `POST`
    - Payload: `{ "city": "city_name" }`
    - Response: Weather prediction for the next three days.

## Contributing

We welcome contributions from the community! To contribute to this project, follow these steps:

1. Fork the repository.
2. Make your changes and commit them.
3. Send a pull request with a description of your changes.


## Contact

For any questions or further information, you can reach out to the project maintainer.
