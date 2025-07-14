from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, CouldNotRetrieveTranscript
import re

def extract_video_id(url_or_id):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
    if match:
        return match.group(1)
    elif len(url_or_id) == 11:
        return url_or_id
    else:
        raise ValueError("Invalid YouTube URL or video ID.")

def fetch_youtube_transcript(url_or_id):
    video_id = extract_video_id(url_or_id)
    print(f"Extracted Video ID: {video_id}")

    try:
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        return " ".join([entry['text'] for entry in transcript])

    except VideoUnavailable:
        raise ValueError("🚫 The video is unavailable or private.")
    
    except TranscriptsDisabled:
        raise ValueError("🛑 Transcripts are disabled for this video.")

    except NoTranscriptFound:
        raise ValueError("❌ No transcript found for this video in any language.")

    except CouldNotRetrieveTranscript:
        raise ValueError("⚠️ Could not retrieve the transcript. Try again later.")

    except Exception as e:
        raise ValueError(f"⚠️ Unexpected error: {str(e)}")
