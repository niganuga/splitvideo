import streamlit as st
import subprocess
import os

def split_video(video_file, split_time):
    # Split the video into two parts
    base_name = os.path.basename(video_file)
    name, ext = os.path.splitext(base_name)
    subprocess.run(["ffmpeg", "-i", video_file, "-t", split_time, "-c", "copy", f"{name}_part1{ext}"])
    subprocess.run(["ffmpeg", "-ss", split_time, "-i", video_file, "-c", "copy", f"{name}_part2{ext}"])

# Title
st.title('Video Splitter')

# Upload the video file
uploaded_file = st.file_uploader("Choose a video...", type=['mp4', 'mkv', 'avi'])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    # Choose the split time
    split_time = st.text_input('Enter split time in HH:MM:SS format', '00:10:00')
    
    if st.button('Split Video'):
        # Save the uploaded file to a temporary location
        video_path = os.path.join('temp', 'temp_video.mp4')
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.read())
        
        # Split the video
        split_video(video_path, split_time)
        
        # Display download links for split videos
        st.write('Download the split videos:')
        st.write(f'[Download Part 1](temp/{os.path.splitext(os.path.basename(video_path))[0]}_part1.mp4)')
        st.write(f'[Download Part 2](temp/{os.path.splitext(os.path.basename(video_path))[0]}_part2.mp4)')
