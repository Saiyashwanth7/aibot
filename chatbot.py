import streamlit as st
import openai
import requests

# Set up API keys
openai.api_key = "YOUR_OPENAI_API_KEY"
weather_api_key = "YOUR_OPENWEATHERMAP_API_KEY"
news_api_key = "YOUR_NEWS_API_KEY"
youtube_api_key = "YOUR_YOUTUBE_API_KEY"

# Function to interact with OpenAI's ChatGPT API
def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to get weather information
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        return response["main"]["temp"], response["weather"][0]["description"]
    return None, "City not found"

# Function to fetch news headlines
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    response = requests.get(url).json()
    articles = response["articles"]
    return [article["title"] for article in articles[:5]]

# Function to search YouTube
def search_youtube(query):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={youtube_api_key}"
    response = requests.get(url).json()
    videos = response.get("items", [])
    return [video["snippet"]["title"] for video in videos[:3]]

# Streamlit App UI
st.title("Multi-API Chatbot")

# User input
user_input = st.text_input("Ask me something!")

# Process user input
if user_input:
    # ChatGPT Response
    st.write("**ChatGPT says:**")
    chatgpt_response = get_chatgpt_response(user_input)
    st.write(chatgpt_response)

    # Check for weather intent
    if "weather" in user_input.lower():
        city = st.text_input("Enter city name for weather:")
        if city:
            temp, desc = get_weather(city)
            if temp:
                st.write(f"The temperature in {city} is {temp}°C with {desc}.")
            else:
                st.write("City not found.")

    # News Intent
    if "news" in user_input.lower():
        st.write("**Top news headlines:**")
        news = get_news()
        for headline in news:
            st.write("- " + headline)

    # YouTube Intent
    if "video" in user_input.lower():
        query = st.text_input("Enter a search query for YouTube:")
        if query:
            videos = search_youtube(query)
            st.write("**Top YouTube videos:**")
            for video in videos:
                st.write("- " + video)
