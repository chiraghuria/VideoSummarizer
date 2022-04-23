import streamlit as st
import numpy as np
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import wave, math, contextlib
import speech_recognition as sr
import moviepy.editor as mp
from moviepy.editor import AudioFileClip
import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import io
import os

st.set_page_config(
    page_title="Video Transcript Summarizer",
    page_icon="🎈",
    layout = "centered"
)

st.title("Video transcript Summarizer!")

def get_summary(text):
    summarizer = pipeline('summarization')

    num_iters = int(len(text)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(text[start:end])[0]['summary_text']
        summarized_text.append(out)
    return summarized_text

with st.form(key="my_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        video_type = st.selectbox(
                "Select video type", ("YouTube", "Video Upload")
            )

    with col2:
        is_research_video = st.selectbox(
                "Research Video", ("Yes", "No")
            )

    youtube_video = st.text_input("YouTube video URL")
    uploaded_video = st.file_uploader(label="Upload your video")
    
    if video_type=="YouTube" and youtube_video is not None:
        submitted = st.form_submit_button(label="Summarize")
        if submitted:
          video_id = youtube_video.split("=")[1]
          transcript = YouTubeTranscriptApi.get_transcript(video_id)
          text = ""
          for i in transcript:
                text += ' ' + i['text']
          
          
          st.write("Preparing your summary...")
          st.write("Transformer at work...")
          summarized_text = get_summary(text)
          
          st.write("SUMMARY")
          st.write(str(summarized_text))

    if video_type=="Video Upload" and uploaded_video is not None:
        submitted = st.form_submit_button(label="Summarize")
        if submitted:
            st.write(uploaded_video)
            g = io.BytesIO(uploaded_video.read())  ## BytesIO Object
            temporary_location = uploaded_video.name

            with open(temporary_location, 'wb') as out:  ## Open temporary file as bytes
                out.write(g.read())  ## Read bytes into file

   
            out.close()
            clip = mp.VideoFileClip(uploaded_video.name) 
            clip.audio.write_audiofile("converted.wav")
            r = sr.Recognizer()
            sound = AudioSegment.from_wav("converted.wav")  
            chunks = split_on_silence(sound,
                min_silence_len = 500,
                silence_thresh = sound.dBFS-14,
                keep_silence=500,
            )
            folder_name = "audio-chunks"
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
            whole_text = ""
            for i, audio_chunk in enumerate(chunks, start=1):
                chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
                audio_chunk.export(chunk_filename, format="wav")
                with sr.AudioFile(chunk_filename) as source:
                    audio_listened = r.record(source)
                    try:
                        text = r.recognize_google(audio_listened)
                    except sr.UnknownValueError as e:
                        print("Error:", str(e))
                    else:
                        text = f"{text.capitalize()}. "
                        whole_text += text
            summarized_text = get_summary(whole_text)
            st.write("SUMMARY")
            st.write(str(summarized_text))

