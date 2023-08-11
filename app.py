import streamlit as st
import subprocess
import os
import speech_recognition as sr

def extract_audio_from_video(video_path, audio_path):
    # Extract audio from the video
    subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"])

def transcribe_audio(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        # Use Google Web Speech API to transcribe the audio
        return r.recognize_google(audio, show_all=True)
    except sr.UnknownValueError:
        return "Google Web Speech API could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Web Speech API; {e}"

# Title
st.title('Video Transcriber')

# Upload the video file
uploaded_file = st.file_uploader("Choose a video...", type=['mp4', 'mkv', 'avi'])

if uploaded_file is not None:
    st.video(uploaded_file)

    if st.button('Generate Transcript'):
        # Ensure the 'temp' directory exists
        if not os.path.exists('temp'):
            os.makedirs('temp')

        # Save the uploaded file to a temporary location
        video_path = os.path.join('temp', 'temp_video.mp4')
        audio_path = os.path.join('temp', 'temp_audio.wav')
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.read())

        # Extract audio from the video
        extract_audio_from_video(video_path, audio_path)

        # Transcribe the audio
        result = transcribe_audio(audio_path)

        if isinstance(result, dict) and 'alternative' in result:
            for idx, transcript in enumerate(result['alternative']):
                st.write(f"Transcript {idx+1}:")
                st.write(transcript['transcript'])
        else:
            st.write(result)
