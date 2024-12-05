import boto3
import requests
import json
import os 

from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WeatherData')

def lambda_handler(event, context):
    city = "London"
    api_key = os.environ['API_KEY'] # Fetching API key from environment variables
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()

    # Process the data
    # Convert temperature from Kelvin to Celsius and set precision to two decimal places
    temperature = Decimal(response["main"]["temp"] - 273.15).quantize(Decimal('0.01'))
    weather = response["weather"][0]["description"]

    # Store to DynamoDB
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    table.put_item(
        Item={
            "date": date,
            "time": time,
            "temperature": temperature,
            "description": weather,
        }
    )

    # Prepare the response data
    weather_data = {
        "date": date,
        "time": time,
        "temperature": float(temperature),  # Convert Decimal to float for JSON serialization
        "description": weather
    }

    return {
        "statusCode": 200,
        "body": json.dumps(weather_data)  # JSON-encode the weather data
    }
