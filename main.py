import requests
from bs4 import BeautifulSoup
import random
import os
import pygame
from flask import Flask, jsonify, send_from_directory
import html
import re

def un_camel_sentence_case(input_string):
    decoded_string = html.unescape(input_string)
    result = re.sub(r'([a-z])([A-Z])', r'\1 \2', decoded_string)  # Add space between lowercase and uppercase
    result = result.replace("_", " ") # replace underscores with spaces
    return result

def get_audio_link():
  # Read champion links from file
  with open("champion_audio_links.txt", "r") as file:
      champion_links = [line.strip() for line in file if line.strip()]

  if not champion_links:
      print("No links found in champion_audio_links.txt")
      exit()

  # Pick a random champion page
  random_champion_url = random.choice(champion_links)

  # Fetch the webpage content
  response = requests.get(random_champion_url)
  if response.status_code != 200:
      print(f"Failed to retrieve {random_champion_url}")
      exit()

  # Parse HTML
  soup = BeautifulSoup(response.text, "html.parser")

  # Find all <audio> tags with class "ext-audiobutton"
  audio_tags = soup.find_all("audio", class_="ext-audiobutton")

  # Extract audio URLs from <source> tags inside <audio> tags
  audio_urls = [tag.find("source")["src"] for tag in audio_tags if tag.find("source")]

  if not audio_urls:
      print(f"No audio files found on {random_champion_url}")
      exit()

  # Pick a random audio file
  random_audio_url = random.choice(audio_urls)

  # Download the audio file
  # audio_file = "temp_audio.ogg"
  # audio_data = requests.get(random_audio_url)
  # with open(audio_file, "wb") as file:
  #     file.write(audio_data.content)

  # Initialize pygame mixer
  # pygame.mixer.init()

  # # Load and play the audio
  # pygame.mixer.music.load(audio_file)
  # pygame.mixer.music.play()

  print(f"Playing: {random_audio_url}")
  return random_audio_url.split(".ogg")[0] + ".ogg"

app = Flask(__name__)
    
@app.route('/')
def home():
    return send_from_directory('', 'index.html')

@app.route('/random-line')
def random_line():
    link = get_audio_link()
    name = un_camel_sentence_case(link.split("/")[-1])[:-4]
    print(name)
    # return jsonify({"oggUrl": "https://static.wikia.nocookie.net/leagueoflegends/images/e/eb/Tristana_Original_BuyItemLastWhisper_0.ogg"})
    return jsonify({"oggUrl": get_audio_link(), "name": name})

if __name__ == '__main__':
    app.run(debug=True)
