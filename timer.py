from moviepy.editor import VideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def make_frame(t):
    # Calculate elapsed time
    elapsed_time = int(t)
    hours = elapsed_time // 3600
    minutes = (elapsed_time % 3600) // 60
    seconds = elapsed_time % 60
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    # Create a blank frame with background color
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Add text to the frame
    font = ImageFont.truetype(font_style, font_size)
    bbox = draw.textbbox((0, 0), time_str, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    draw.text(((width - text_width) / 2, (height - text_height) / 2), time_str, font=font, fill=font_color)
    
    # Convert PIL Image to numpy array
    frame = np.array(img)
    return frame

# Settings
width, height = 640, 1080
bg_color = (255, 202, 0)  # Black background
font_color = (255, 255, 255)  # White font
font_style = "C:\\Users\\user\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Bangers-Regular.ttf"  # Path to a font file
font_size = 150
duration = 10  # 3 hours in seconds

# Create the video
video_clip = VideoClip(make_frame, duration=duration)
video_clip.write_videofile("2.5k.mp4", fps=24)