import os
import yt_dlp
import uuid
import imageio_ffmpeg
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Add ffmpeg to PATH so yt-dlp can find it
os.environ["PATH"] += os.pathsep + os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())

class AudioDownloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def extract_video_id(self, url):
        """Extracts video ID from YouTube URL."""
        parsed = urlparse(url)
        if parsed.hostname == 'youtu.be':
            return parsed.path[1:]
        if parsed.hostname in ('www.youtube.com', 'youtube.com'):
            if parsed.path == '/watch':
                p = parse_qs(parsed.query)
                return p['v'][0]
            if parsed.path[:7] == '/embed/':
                return parsed.path.split('/')[2]
            if parsed.path[:3] == '/v/':
                return parsed.path.split('/')[2]
        return None

    def get_transcript(self, url):
        """Attempts to fetch existing transcript from YouTube."""
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return None
            
            print(f"Attempting to fetch captions for Video ID: {video_id}...")
            # Try fetching transcript list (defaults to English or auto-generated)
            # We try to get 'en' or auto-generated
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'ta', 'ta-IN']) 
            
            # Combine text
            full_text = " ".join([t['text'] for t in transcript_list])
            return full_text
        except Exception as e:
            print(f"Could not fetch transcript via API: {e}")
            return None

    def download_audio(self, url):
        """
        Downloads audio from a YouTube URL and returns the file path.
        """
        try:
            # Generate a unique filename
            filename = str(uuid.uuid4())
            
            ydl_opts = {
                'format': 'bestaudio/best',
                # We remove explicit ffmpeg location/post-processing to avoid needing ffprobe
                # faster-whisper can decode m4a/webm directly if ffmpeg is in PATH (which we handled via os.environ)
                'outtmpl': os.path.join(self.output_dir, f'{filename}.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the actual filename that was written
                final_path = ydl.prepare_filename(info)
                
                # Verify it exists
                if not os.path.exists(final_path):
                    # Fallback: check if the 'ext' in info matches what's on disk
                    # Sometimes prepare_filename might not be 100% accurate if yt-dlp merged formats (unlikely here)
                    # Let's search for the UUID in the download dir
                    for f in os.listdir(self.output_dir):
                        if filename in f:
                            final_path = os.path.join(self.output_dir, f)
                            break
                
                print(f"Audio downloaded to: {final_path}")
                return final_path, info.get('title', 'Unknown Title')
        
        except Exception as e:
            print(f"Error downloading audio: {e}")
            raise e
