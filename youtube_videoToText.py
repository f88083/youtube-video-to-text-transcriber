from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from openai import OpenAI
import constants

def select_directory():
    """Open a directory selection dialog and return the selected path."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(
        initialdir=str(Path.home() / "Downloads"),
        title="Select Download Directory"
    )

def get_valid_filename(title):
    """Convert string to a valid filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    filename = ''.join(char if char not in invalid_chars else '_' for char in title)
    return filename.strip()

def transcribe_audio(audio_path, output_dir, delete_after=False):
    """Transcribe audio file using OpenAI's Whisper model."""
    try:
        # Create OpenAI client
        client = OpenAI(api_key=constants.API_KEY)
        
        # Open and transcribe the audio file
        with open(audio_path, "rb") as audio_file:
            print("\nTranscribing audio... This may take a while...")
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        # Create transcription filename based on original audio filename
        audio_filename = Path(audio_path).stem
        transcript_path = Path(output_dir) / f"{audio_filename}_transcript.txt"
        
        # Save transcription
        with open(transcript_path, "w", encoding='utf-8') as file:
            file.write(transcription.text)
        
        print(f"\nTranscription completed successfully!")
        print(f"Transcript saved as: {transcript_path}")
        
        # Delete the audio file if requested
        if delete_after and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Temporary audio file deleted.")
            
        return True
        
    except Exception as e:
        print(f"\nTranscription error: {str(e)}")
        if "api_key" in str(e).lower():
            print("Please check if your OpenAI API key is correctly set in constants.py")
        return False

def process_youtube_audio():
    try:
        # Get URL from user
        url = input("Please enter the YouTube video URL: ").strip()
        if not url:
            print("URL cannot be empty.")
            return
        
        # Create a YouTube object
        print("Fetching video information...")
        yt = YouTube(url, on_progress_callback=on_progress)
        
        # Get video title and create valid filename
        title = get_valid_filename(yt.title)
        print(f"\nVideo title: {title}")
        
        # Ask user for desired action
        print("\nWhat would you like to do?")
        print("1. Download audio only")
        print("2. Transcribe only (no local audio save)")
        print("3. Download audio and transcribe")
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        if choice not in ['1', '2', '3']:
            print("Invalid choice. Please try again.")
            return
        
        # Get audio stream
        print("\nGetting audio stream...")
        audio = yt.streams.get_audio_only()
        
        # Show file size
        file_size = audio.filesize / (1024 * 1024)  # Convert to MB
        print(f"Audio file size: {file_size:.2f} MB")
        
        # Handle different choices
        if choice in ['1', '3']:  # Download audio
            # Get download directory from user
            print("\nSelect download directory (a file dialog will open)")
            print("Press Cancel in the dialog to use the default Downloads directory")
            
            selected_dir = select_directory()
            download_dir = selected_dir if selected_dir else str(Path.home() / "Downloads")
            print(f"Selected directory: {download_dir}")
            
            # Create directory if it doesn't exist
            download_path = Path(download_dir)
            download_path.mkdir(parents=True, exist_ok=True)
            
            # Get filename from user
            default_filename = f"{title}.mp3"
            custom_filename = input(f"\nEnter filename (press Enter for default '{default_filename}'): ").strip()
            if not custom_filename:
                custom_filename = default_filename
            elif not custom_filename.endswith('.mp3'):
                custom_filename += '.mp3'
            
            # Check if file already exists
            full_path = download_path / custom_filename
            if full_path.exists():
                overwrite = input("File already exists. Overwrite? (y/n): ").lower()
                if overwrite != 'y':
                    print("Operation cancelled.")
                    return
            
            # Download the audio
            print("\nDownloading audio...")
            audio.download(filename=custom_filename, output_path=str(download_path))
            print(f"\nDownload completed successfully!")
            print(f"File saved as: {full_path}")
            
            # Handle transcription for choice 3
            if choice == '3':
                transcribe = input("\nProceed with transcription? (y/n): ").lower()
                if transcribe == 'y':
                    transcribe_audio(str(full_path), str(download_path))
        
        else:  # Transcribe only (choice 2)
            # Create temporary directory for audio, use Desktop
            temp_dir = str(Path.home() / "Desktop")
            temp_audio_path = os.path.join(temp_dir, f"{title}.mp3")
            
            # Download to temporary location
            print("\nDownloading audio to temporary location...")
            audio.download(filename=title + ".mp3", output_path=temp_dir)
            
            # Get transcription save location
            print("\nSelect where to save the transcription:")
            trans_dir = select_directory() or str(Path.home() / "Downloads")
            
            # Transcribe and auto-delete temporary file
            transcribe_audio(temp_audio_path, trans_dir, delete_after=True)
    
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        if "Video unavailable" in str(e):
            print("The video might be private or deleted.")
        elif "regex_search" in str(e):
            print("Invalid YouTube URL. Please check the URL and try again.")

if __name__ == "__main__":
    print("YouTube Audio Processor")
    print("=" * 40)
    print("Note: For transcription, make sure you have:")
    print("1. OpenAI API key set in constants.py")
    print("2. Required packages installed (openai)")
    
    while True:
        process_youtube_audio()
        
        # Ask if user wants to process another video
        again = input("\nWould you like to process another video? (y/n): ").lower()
        if again != 'y':
            print("\nThank you for using YouTube Audio Processor!")
            break