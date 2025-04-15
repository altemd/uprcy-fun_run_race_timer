from moviepy.editor import VideoClip, AudioFileClip, CompositeAudioClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

rcylogo = Image.open("C:\\Users\\user\\Downloads\\UP RCY Logo.png")
# Resize the logo if needed
desired_height = 300
aspect_ratio = rcylogo.width / rcylogo.height
desired_width = int(desired_height * aspect_ratio)
rcylogo = rcylogo.resize((desired_width, desired_height), Image.LANCZOS)
desired_height = 350
bloodlinelogo = Image.open("C:\\Users\\user\\Downloads\\Blood Line Logo.png")
aspect_ratio = bloodlinelogo.width / bloodlinelogo.height
desired_width = int(desired_height * aspect_ratio)
bloodlinelogo = bloodlinelogo.resize((desired_width, desired_height), Image.LANCZOS)


def make_frame(t):
    # Create a blank frame with background color
    img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Timer logic and rendering for each section
    timers = [
        create_left_timer(t),
        create_middle_timer(t),
        create_right_timer(t)
    ]

    # Add each timer to the frame
    labels = ["10K Time", "5K Time", "2.5K Time"]  # Modify these labels as needed
    for i, ((time_str, bg_color, font_color, shadow_color), label) in enumerate(zip(timers, labels)):
        sub_img = create_timer_image(time_str, bg_color, font_color, shadow_color, label)
        img.paste(sub_img, (i * (width // 3), 0))
        
    # Add logo to the top left
    img.paste(rcylogo, (((width - rcylogo.width) // 2 + 175), 10) , rcylogo)  # The third argument allows for transparency if the logo has an alpha channel
    img.paste(bloodlinelogo, (((width - bloodlinelogo.width) // 2 - 140), 10), bloodlinelogo)

    # Convert PIL Image to numpy array
    frame = np.array(img)
    return frame

def create_left_timer(t):
    elapsed_time = int(t)
    remaining_time = 300 - int(t)
    if remaining_time > 0:
        hours, minutes, seconds = seconds_to_hms(remaining_time)
        time_str = f"-{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        hours, minutes, seconds = seconds_to_hms(elapsed_time-300)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_str, (255, 48, 54), (255, 255, 255), (0, 0, 0)

def create_middle_timer(t):
    elapsed_time = int(t)
    remaining_time = 900 - int(t) + 300
    #hours, minutes, seconds = seconds_to_hms(elapsed_time-5)
    if remaining_time > 0:
        hours, minutes, seconds = seconds_to_hms(remaining_time)
        time_str = f"-{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        hours, minutes, seconds = seconds_to_hms(elapsed_time-900-300)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_str, (78, 183, 249), (255, 255, 255), (0, 0, 0)

def create_right_timer(t):
    elapsed_time = int(t)
    remaining_time = 1800 - int(t) + 300
    #hours, minutes, seconds = seconds_to_hms(elapsed_time-10)
    if remaining_time > 0:
        hours, minutes, seconds = seconds_to_hms(remaining_time)
        time_str = f"-{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        hours, minutes, seconds = seconds_to_hms(elapsed_time-1800-300)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return time_str, (255, 202, 0), (255, 255, 255), (0, 0, 0)

def seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return hours, minutes, seconds

def create_timer_image(time_str, bg_color, font_color, shadow_color, label_text):
    sub_img = Image.new('RGB', (width // 3, height), bg_color)
    sub_draw = ImageDraw.Draw(sub_img)
    font = ImageFont.truetype(font_style, font_size)
    bbox = sub_draw.textbbox((0, 0), time_str, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    shadow_offset = 10

    # Draw shadow text
    sub_draw.text(
        ((width // 3 - text_width) / 2 + shadow_offset, (height - text_height) / 2 + shadow_offset),
        time_str,
        font=font,
        fill=shadow_color
    )

    # Draw main text
    sub_draw.text(
        ((width // 3 - text_width) / 2, (height - text_height) / 2),
        time_str,
        font=font,
        fill=font_color
    )
    
    label_font = ImageFont.truetype(font_style, font_size // 2)  # Smaller font for label
    label_bbox = sub_draw.textbbox((0, 0), label_text, font=label_font)
    label_width = label_bbox[2] - label_bbox[0]
    label_height = label_bbox[3] - label_bbox[1]
    shadow_offset = 5
    
    sub_draw.text(
        ((width // 3 - label_width) / 2 + shadow_offset, (height + text_height) / 2 + shadow_offset + 50),
        label_text,
        font=label_font,
        fill=shadow_color
    )

    # Draw label text
    sub_draw.text(
        ((width // 3 - label_width) / 2, (height + text_height) / 2 + 50),
        label_text,
        font=label_font,
        fill=font_color
    )
    
    
    
    border_width = 4  # Adjust this value to change border thickness
    sub_draw.rectangle([0, 0, width // 3 - 1, height - 1], outline=(255, 255, 255), width=border_width)

    return sub_img

# Settings
width, height = 1920, 1080
font_style = "C:\\Users\\user\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Bangers-Regular.ttf"
font_size = 150
duration = 10801 + 300

# Audio settings
audio_file_path = "C:\\Users\\user\\Desktop\\funrun\\timer\\Countdown 1.wav"
audio_play_times = [300-3, 1200-3, 2100-3]

def create_audio(duration):
    audio_clips = []
    base_audio = AudioFileClip(audio_file_path)
    
    for play_time in audio_play_times:
        if play_time < duration:
            audio_clips.append(base_audio.set_start(play_time))
    
    return CompositeAudioClip(audio_clips)


# Create the main video clip
main_clip = VideoClip(make_frame, duration=5)

# Create the audio
audio_clip = create_audio(duration)

# Combine all clips
final_clip = CompositeVideoClip([main_clip])

# Set the audio of the video
final_clip = final_clip.set_audio(audio_clip)

# Write the final video file
final_clip.write