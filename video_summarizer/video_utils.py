from pathlib import Path
import tempfile

def save_temp_video(video_file):
    """Save uploaded video to a temporary file and return its path."""
    # Extract the original file extension
    original_name = getattr(video_file, 'name', None)
    ext = Path(original_name).suffix if original_name else '.mp4'
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_video:
        temp_video.write(video_file.read())
        return temp_video.name

def cleanup_temp_file(file_path):
    """Delete the temporary video file."""
    Path(file_path).unlink(missing_ok=True)
