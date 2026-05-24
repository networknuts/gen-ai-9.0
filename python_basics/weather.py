import requests 

weather_api_key = "REPLACE_WITH_YOUR_API_KEY"
weather_zip_code = input("Enter your zip code: ")
weather_country_code = input("Enter your country code: ")


weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?zip={weather_zip_code},{weather_country_code}&appid={weather_api_key}"

response = requests.get(weather_api_url)
print(response.json())