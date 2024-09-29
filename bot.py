import os
import json
import requests
import time
from telegram import Bot

# Your API token and channel ID
API_TOKEN = '8140181108:AAErw9qQcDoOjyYkIh-7TDQUcLhTzxt8pM0'
CHANNEL_ID = -1002278664533  # Your channel ID

# Initialize Telegram bot
bot = Bot(token=API_TOKEN)

# Function to fetch the JSON data
def fetch_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching JSON: {e}")
        return None

# Function to send message to Telegram channel
def send_message(event_name, match_name, stream_link, src):
    caption = f"*{event_name}*\n\n*Match:* {match_name}\n*Stream Link:* {stream_link}"
    bot.send_photo(chat_id=CHANNEL_ID, photo=src, caption=caption, parse_mode='Markdown')

# URL of the JSON file to monitor
json_url = 'https://raw.githubusercontent.com/drmlive/fancode-live-events/main/fancode.json'  # Replace with your actual JSON URL

# Initialize previous stream link to None
previous_stream_link = None

# Continuously check for updates
while True:
    data = fetch_json(json_url)
    if data:
        # Extract the relevant data from JSON
        event_name = data.get('event_name')
        match_name = data.get('match_name')
        stream_link = data.get('stream_link')
        src = data.get('src')

        # Check if the stream link has changed
        if stream_link != previous_stream_link:
            send_message(event_name, match_name, stream_link, src)
            previous_stream_link = stream_link  # Update the previous stream link

    # Wait for a specified interval before checking again (e.g., 30 seconds)
    time.sleep(30)
  
