# YouTube Audio Processor

A Python application that allows you to download YouTube videos as audio files and transcribe them to text using OpenAI's Whisper model. This tool offers flexible options for processing YouTube content, whether you want to save the audio locally, get a transcription, or both.

## Features

- **Download YouTube Audio**: Extract audio from YouTube videos and save them as MP3 files
- **Audio Transcription**: Convert audio to text using OpenAI's Whisper model
- **Flexible Processing Options**:
  - Download audio only
  - Transcribe without saving audio locally
  - Download audio and transcribe
- **User-Friendly Interface**:
  - Graphical directory selection
  - Progress tracking during download
  - File overwrite protection
  - Custom filename support
- **Error Handling**:
  - Invalid URL detection
  - Permission error handling
  - API key validation
  - File system error handling

## Prerequisites

- Python 3.6 or higher
- OpenAI API key
- Required Python packages:
  - pytubefix
  - openai
  - tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-audio-processor.git
cd youtube-audio-processor
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `constants.py` file in the project directory:
```python
API_KEY = "your-openai-api-key-here"
```

## Usage

1. Run the script:
```bash
python youtube_processor.py
```

2. Enter the YouTube video URL when prompted.

3. Choose your desired processing option:
   - Option 1: Download audio only
   - Option 2: Transcribe only (no local audio save)
   - Option 3: Download audio and transcribe

4. Follow the prompts to:
   - Select save location (using file dialog)
   - Customize filename (optional)
   - Confirm operations

## Example Usage

```python
# Download and transcribe a YouTube video
$ python youtube_videoToText.py

YouTube Audio Processor
========================================
Note: For transcription, make sure you have:
1. OpenAI API key set in constants.py
2. Required packages installed (openai)

Please enter the YouTube video URL: https://www.youtube.com/watch?v=example

Video title: Example Video

What would you like to do?
1. Download audio only
2. Transcribe only (no local audio save)
3. Download audio and transcribe

Enter your choice (1/2/3): 3
```

## File Structure

```
youtube-audio-processor/
│
├── tools/ # Some unused codes
├── test/ # For test purposes
├── youtube_videoToText.py   # Main script
├── constants.py          # API key configuration
└── README.md            # Documentation
```

## Key Functions

- `select_directory()`: Opens a file dialog for directory selection
- `get_valid_filename()`: Sanitizes filenames for system compatibility
- `transcribe_audio()`: Handles audio transcription using OpenAI's Whisper
- `process_youtube_audio()`: Main function managing the download and transcription process

## Error Handling

The script includes comprehensive error handling for:
- Invalid YouTube URLs
- Network connection issues
- File system permissions
- API authentication
- Invalid user input

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://openai.com/research/whisper) for audio transcription
- [pytubefix](https://github.com/JuanBindez/pytubefix) for YouTube video processing

## Disclaimer

This tool is for educational and personal use only. Please respect YouTube's terms of service and content creators' rights when using this application.

## Support

For support, please open an issue in the GitHub repository or contact by [email](mailto:sc.lai.simon@gmail.com).

---
Created by SimonLai23 - Feel free to contact me!
