import streamlit as st
from config_utils import load_and_configure_api
from agent_utils import initialize_agent
from video_utils import save_temp_video, cleanup_temp_file
from prompt_utils import build_analysis_prompt

# Load and configure API
try:
    load_and_configure_api()
except Exception as e:
    st.error(f"API configuration error: {e}")
    st.stop()

# Streamlit page configuration
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="🎥",
    layout="wide"
)


st.title("Agno Video AI Summarizer Agent 🎥🎤🔬")
st.header("Powered by Gemini 2.0 Flash Exp")

# Initialize the agent (cached)
@st.cache_resource
def get_agent():
    return initialize_agent()

multimodal_agent = get_agent()

# File uploader for video files
video_file = st.file_uploader(
    "Upload a video file", type=['mp4', 'mov', 'avi'],
    help="Upload a video for AI analysis"
)

if video_file:
    video_path = save_temp_video(video_file)
    st.video(video_path, format="video/mp4", start_time=0)

    user_query = st.text_area(
        "What insights are you seeking from the video?",
        placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
        help="Provide specific questions or insights you want from the video."
    )

    if st.button("🔍 Analyze Video", key="analyze_video_button"):
        if not user_query:
            st.warning("Please enter a question or insight to analyze the video.")
        else:
            try:
                with st.spinner("Processing video and gathering insights..."):
                    analysis_prompt = build_analysis_prompt(user_query)
                    from agno.media import Video
                    with open(video_path, "rb") as video_file_obj:
                        video_data = video_file_obj.read()
                        import os
                        file_ext = os.path.splitext(video_path)[1][1:].lower()  # e.g., 'mp4', 'mov', 'avi'
                        video_media = Video(content=video_data, format=file_ext)
                        response = multimodal_agent.run(analysis_prompt, videos=[video_media])

                st.subheader("Analysis Result")
                st.markdown(response.content)

            except Exception as error:
                st.error(f"An error occurred during analysis: {error}")
            finally:
                if 'video_path' in locals():
                    cleanup_temp_file(video_path)
else:
    st.info("Upload a video file to begin analysis.")

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
