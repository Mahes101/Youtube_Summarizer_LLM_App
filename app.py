import streamlit as st 
from dotenv import load_dotenv

load_dotenv()
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """
    You are a youtube summarizer. You will be taking a youtube video transcript text and summarizing the entire video and providing 
    important points of the video within 250 words. Please provide the transcript text of the video here: 
"""
def extract_transcript_video(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ""
        for item in transcript:
            transcript_text += item["text"] + " "
        return transcript_text
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None


def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(prompt+transcript_text)
    return response.text 


## Streamlit UI Framework
st.title("Youtube Transcript Summarizer")
youtube_video_url = st.text_input("Enter the youtube video url here")
if youtube_video_url:
    video_id = youtube_video_url.split("v=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
if st.button("Get Detailed Summary"):
    st.write("Generating detailed summary...")    
    transcript_text = extract_transcript_video(youtube_video_url)
    if transcript_text:
        response = generate_gemini_content(transcript_text, prompt)
        st.write("Detailed Summary: ")
        st.write(response)