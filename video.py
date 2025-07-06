from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
import streamlit as st
import os
import tempfile
import whisper
from moviepy.editor import VideoFileClip
from phi.tools.youtube_tools import YouTubeTools

load_dotenv()

# Setup Groq Agent
model = Groq(
    id="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY")
)

agent = Agent(
    model=model,
    tools=[YouTubeTools()],
    show_tool_calls=True,
    description="You are a YouTube/video analysis agent. Generate summaries from links or uploads.",
)


def summarize_youtube_video(link):
    prompt = f"""
    You are given a YouTube video link: {link}

    Your task is to:
    1. Extract the *title, **author, and **thumbnail*.
    2. Fetch captions or transcript (if available).
    3. Generate a *detailed summary*:
       - What is the video about?
       - Key points and topics discussed.
       - Intended audience and tone.

    Format output in clear *Markdown*.
    """
    output = agent.run(prompt, markdown=True)
    return output.content

# # Function for summarizing uploaded video files
# def summarize_uploaded_video(uploaded_file):
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
#         tmp_video.write(uploaded_file.read())
#         tmp_video_path = tmp_video.name

    # Extract audio
    # audio_path = tmp_video_path.replace(".mp4", ".mp3")
    # video = VideoFileClip(tmp_video_path)
    # video.audio.write_audiofile(audio_path)

    # Transcribe with Whisper
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    transcript = result["text"]

    # Summarize the transcript using the LLM
    prompt = f"""
    Below is the transcript of a user-uploaded video:

    {transcript}

    Summarize this in detail:
    - Key topics discussed
    - Educational or entertainment purpose
    - Target audience
    - Tone and overall message

    Present the summary in clean, readable *Markdown* format.
    """
    output = agent.run(prompt, markdown=True)
    return output.content


# === Streamlit UI ===
def main():
    st.markdown("""
        <div style="background: linear-gradient(to right, #00b4db, #0083b0); padding: 20px; border-radius: 10px;">
            <h2 style="color: white; text-align: center;">
                🎬 YouTube Video Summary Extractor
            </h2>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📎 Option 1: Paste a YouTube Link")
    link = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

    # st.markdown("### 📁 Option 2: Upload a Video File (MP4 only)")
    # uploaded_file = st.file_uploader("Upload your video", type=["mp4"])

    st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: #DD3300;
            color: #fff;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5em 1.5em;
        }
        div.stButton > button:first-child:hover {
            background-color: #bb2200;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("🧠 Generate Summary"):
        if link:
            with st.spinner("Processing YouTube video..."):
                summary = summarize_youtube_video(link)
            st.success("✅ Summary generated from YouTube link!")
            st.markdown(summary, unsafe_allow_html=True)

        elif uploaded_file:
            with st.spinner("Processing uploaded video..."):
                summary = summarize_uploaded_video(uploaded_file)
            st.success("✅ Summary generated from uploaded file!")
            st.markdown(summary, unsafe_allow_html=True)

        else:
            st.warning("⚠ Please provide either a YouTube link or upload a video.")

if _name_ == "_main_":
    main()