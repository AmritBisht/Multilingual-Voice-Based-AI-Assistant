import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import queue
import threading

# Configure the page
st.set_page_config(page_title="Multilingual AI Assistant", layout="wide")


# Load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize conversation memory
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Language options
LANGUAGE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh"
}

# WebRTC-based live voice input
def voice_input():
    st.info("🎙️ Click 'Start Recording' and speak.")

    recognizer = sr.Recognizer()
    audio_queue = queue.Queue()

    def process_audio(audio_data):
        try:
            with sr.AudioFile(audio_data) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            return "❗ Could not understand audio."
        except sr.RequestError as e:
            return f"❗ Recognition error: {e}"

    webrtc_ctx = webrtc_streamer(
        key="speech",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        async_processing=True,
    )

    if webrtc_ctx.audio_receiver:
        audio_data = webrtc_ctx.audio_receiver.get_frame(timeout=10)
        if audio_data:
            text = process_audio(audio_data)
            st.success(f"🗣️ You said: {text}")
            return text

    return None

# Generate AI response using Gemini
def generate_ai_response(user_text):
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Prepare context with last 6 interactions
    conversation_context = "\n".join(st.session_state.conversation_history[-6:])
    prompt = f"{conversation_context}\nUser: {user_text}\nAI:"

    try:
        response = model.generate_content(prompt)
        ai_response = response.text

        # Store conversation in memory
        st.session_state.conversation_history.append(f"User: {user_text}")
        st.session_state.conversation_history.append(f"AI: {ai_response}")

        return ai_response
    except Exception as e:
        st.error(f"❗ AI Error: {e}")
        return "I'm sorry, there was an error generating a response."

# Convert AI response to speech
def text_to_speech(text, language='en'):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("speech.mp3")
        return "speech.mp3"
    except Exception as e:
        st.error(f"❗ Error generating speech: {e}")
        return None

# Display chat messages
def display_chat():
    st.markdown("""
        <style>
            .chat-container {
                height: 450px;
                overflow-y: auto;
                border-radius: 10px;
                border: 1px solid #ccc;
                padding: 15px;
                background-color: #F9F9F9;
            }
            .user-message {
                background-color: #DCF8C6;
                padding: 12px;
                border-radius: 20px;
                margin-bottom: 10px;
                text-align: right;
                color: #333;
                max-width: 70%;
                margin-left: auto;
            }
            .ai-message {
                background-color: #E5E5EA;
                padding: 12px;
                border-radius: 20px;
                margin-bottom: 10px;
                text-align: left;
                color: #333;
                max-width: 70%;
                margin-right: auto;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.conversation_history:
        if msg.startswith("User:"):
            st.markdown(f"<div class='user-message'>{msg.replace('User: ', '')}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='ai-message'>{msg.replace('AI: ', '')}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main app
def main():

    st.markdown("<h1 style='text-align: center; font-size: 40px; color: #1F51FF;'>🌐 Multilingual Voice-Based AI Assistant</h1>", unsafe_allow_html=True)

    # Language selection
    col1, col2 = st.columns(2)
    with col1:
        input_lang_name = st.selectbox("🌍 Select Input Language:", list(LANGUAGE_MAP.keys()))
    with col2:
        output_lang_name = st.selectbox("🌍 Select Output Language:", list(LANGUAGE_MAP.keys()))

    input_lang = LANGUAGE_MAP[input_lang_name]
    output_lang = LANGUAGE_MAP[output_lang_name]

    # Display chat
    display_chat()

    # Choose Voice or Text Input
    input_method = st.radio("🎤 Choose Input Method:", ["Voice", "Text"])

    # Capture User Input (Voice or Text)
    user_text = ""

    if input_method == "Voice":
        user_text = voice_input()
    else:
        user_text = st.text_input("✍️ Type your message here")
        if st.button("Send") and user_text.strip():
            pass  # Proceed with AI processing

    # Process and Display AI Response
    if user_text:
        with st.spinner("🧠 Generating AI Response..."):
            response_text = generate_ai_response(user_text)

        st.empty()  # Clear spinner

        if response_text:
            with st.spinner("🔊 Converting AI Response to Speech..."):
                audio_file = text_to_speech(response_text, language=output_lang)

            st.empty()

            # Display AI Response
            st.markdown(f"**🤖 AI Response:** {response_text}")

            # Play and Download Audio
            if audio_file:
                with open(audio_file, "rb") as audio:
                    audio_bytes = audio.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("📥 Download AI Response", data=audio_bytes, file_name="response.mp3", mime="audio/mp3")
        else:
            st.error("❗ No response generated by the AI.")

# Run the app
if __name__ == "__main__":
    main()
