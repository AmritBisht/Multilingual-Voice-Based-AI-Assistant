import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import streamlit as st

# Configure the page
st.set_page_config(page_title="Multilingual AI Assistant", layout="wide")

# Load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize conversational memory
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

# Record audio using sounddevice
def record_audio(duration=5, samplerate=44100, channels=1):
    try:
        st.info("🎙️ Recording... Please speak.")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
        sd.wait()
        st.success("✅ Recording complete.")
        wav.write("input_audio.wav", samplerate, audio_data)
        return "input_audio.wav"
    except Exception as e:
        st.error(f"❗ Error during recording: {e}")
        return None

# Convert AI response to speech
def text_to_speech(text, language='en'):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save("speech.mp3")
        st.success("🔊 Speech generated successfully!")
    except Exception as e:
        st.error(f"❗ Error generating speech: {e}")

# Generate AI response using Gemini with memory
def llm_model_object(user_text):
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Prepare prompt with conversational memory (up to 6 previous interactions)
    conversation_context = "\n".join(st.session_state.conversation_history[-6:])
    prompt = f"{conversation_context}\nUser: {user_text}\nAI:"

    try:
        response = model.generate_content(prompt)
        ai_response = response.text

        # Store messages in memory
        st.session_state.conversation_history.append(f"User: {user_text}")
        st.session_state.conversation_history.append(f"AI: {ai_response}")

        return ai_response
    except Exception as e:
        st.error(f"❗ Error from Gemini AI: {e}")
        return "I'm sorry, there was an error generating a response."

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
    st.markdown("<h1 style='text-align: center; font-size: 60px; color: #1F51FF;'>🌐 Multilingual AI Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; font-size: 16px; color: #606060;'>Powered by Google Gemini AI and Speech Recognition</h4>", unsafe_allow_html=True)

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

    user_text = ""
    if input_method == "Voice":
        if st.button("🎙️ Start Speaking"):
            audio_file = record_audio()
            if audio_file:
                st.success("✅ Audio recorded successfully! Now converting to text...")
                # Using speech recognition to convert audio to text
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)
                    try:
                        user_text = recognizer.recognize_google(audio, language=input_lang)
                        st.success(f"🗣️ You said: {user_text}")
                    except Exception as e:
                        st.error(f"❗ Speech recognition failed: {e}")

    else:
        user_text = st.text_input("✍️ Type your message here")
        if st.button("Send"):
            if not user_text.strip():
                st.warning("❗ Please enter a valid message.")

    # Process and Display AI Response
    if user_text:
        with st.spinner("🧠 Generating AI Response..."):
            response_text = llm_model_object(user_text)
        
        st.empty()  # Clear spinner

        if response_text:
            with st.spinner("🔊 Converting AI Response to Speech..."):
                text_to_speech(response_text, language=output_lang)

            st.empty()

            # Display response
            st.markdown(f"**🤖 AI Response:** {response_text}")

            # Audio playback
            try:
                with open("speech.mp3", "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("📥 Download AI Response", data=audio_bytes, file_name="response.mp3", mime="audio/mp3")
            except FileNotFoundError:
                st.error("❗ Error: Audio file not found.")
        else:
            st.error("❗ No response generated by the AI.")

# Run the app
if __name__ == "__main__":
    main()
