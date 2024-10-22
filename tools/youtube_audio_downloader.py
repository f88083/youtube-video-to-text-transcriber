from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

def select_directory():
    """Open a directory selection dialog and return the selected path."""
    # Create and hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Open the directory selection dialog
    directory = filedialog.askdirectory(
        initialdir=str(Path.home() / "Downloads"),
        title="Select Download Directory"
    )
    
    return directory

def get_valid_filename(title):
    """Convert string to a valid filename by removing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    filename = ''.join(char if char not in invalid_chars else '_' for char in title)
    return filename.strip()

def download_youtube_audio():
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
        
        # Get download directory from user
        default_dir = str(Path.home() / "Downloads")
        print("\nSelect download directory (a file dialog will open)")
        print(f"Default directory: {default_dir}")
        print("Press Cancel in the dialog to use the default directory")
        
        # Open directory selection dialog
        selected_dir = select_directory()
        download_dir = selected_dir if selected_dir else default_dir
        print(f"Selected directory: {download_dir}")
        
        # Convert to Path object for better path handling
        download_path = Path(download_dir)
        
        # Create directory if it doesn't exist
        try:
            download_path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"Error: No permission to create directory at {download_dir}")
            return
        except Exception as e:
            print(f"Error creating directory: {str(e)}")
            return
        
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
                print("Download cancelled.")
                return
        
        # Get audio stream
        print("\nGetting audio stream...")
        audio = yt.streams.get_audio_only()
        
        # Show file size
        file_size = audio.filesize / (1024 * 1024)  # Convert to MB
        print(f"Audio file size: {file_size:.2f} MB")
        
        # Confirm download
        confirm = input("\nProceed with download? (y/n): ").lower()
        if confirm != 'y':
            print("Download cancelled.")
            return
        
        # Download the audio
        print("\nDownloading audio...")
        audio.download(filename=custom_filename, output_path=str(download_path))
        
        print(f"\nDownload completed successfully!")
        print(f"File saved as: {full_path}")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        if "Video unavailable" in str(e):
            print("The video might be private or deleted.")
        elif "regex_search" in str(e):
            print("Invalid YouTube URL. Please check the URL and try again.")

if __name__ == "__main__":
    print("YouTube Audio Downloader")
    print("=" * 30)
    print("Note: This program will open a file dialog for selecting the download directory.")
    while True:
        download_youtube_audio()
        
        # Ask if user wants to download another video
        again = input("\nWould you like to download another video? (y/n): ").lower()
        if again != 'y':
            print("\nThank you for using YouTube Audio Downloader!")
            break