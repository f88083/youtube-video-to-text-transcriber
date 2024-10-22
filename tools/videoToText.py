import os
import constants
from openai import OpenAI

# Create an api client
client = OpenAI(api_key=constants.API_KEY)

# Desktop path
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop");

# audio file name
audio_file_name = "0050也藏有ROE.m4a"

# Load audio file
audio_file= open(f"{desktop_path}/{audio_file_name}", "rb")

# Transcribe
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)

# Output the transciption to the file
with open(f"{desktop_path}/transcription.txt", "w") as file:
    file.write(transcription.text)
