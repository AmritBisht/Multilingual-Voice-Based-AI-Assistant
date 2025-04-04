import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode,AudioProcessorBase
import queue
import threading
import av

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
audio_queue = queue.Queue()

class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray().flatten().astype(np.float32).tobytes()
        audio_queue.put(audio)
        return frame

def capture_audio_from_queue():
    recognizer = sr.Recognizer()
    st.info("🎙️ Listening... Please speak clearly.")

    audio_data = b""
    try:
        # Wait for audio
        for _ in range(50):  # adjust the range/time as needed
            audio_chunk = audio_queue.get(timeout=0.5)
            audio_data += audio_chunk
    except queue.Empty:
        st.warning("❗ No audio input detected.")
        return None

    try:
        # Save audio temporarily
        with open("temp.wav", "wb") as f:
            f.write(audio_data)

        with sr.AudioFile("temp.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            st.success(f"🗣️ You said: {text}")
            return text
    except Exception as e:
        st.error(f"❗ Speech recognition failed: {e}")
        return None

# === 🧠 AI Chat Function ===

def generate_ai_response(user_text):
    model = genai.GenerativeModel('gemini-2.0-flash')
    context = "\n".join(st.session_state.conversation_history[-6:])
    prompt = f"{context}\nUser: {user_text}\nAI:"
    try:
        response = model.generate_content(prompt)
        ai_response = response.text
        st.session_state.conversation_history += [f"User: {user_text}", f"AI: {ai_response}"]
        return ai_response
    except Exception as e:
        return f"❗ AI Error: {e}"

def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("response.mp3")
        return "response.mp3"
    except Exception as e:
        st.error(f"Text-to-speech error: {e}")
        return None

def display_chat():
    st.markdown("<div style='height:400px;overflow:auto;border:1px solid #ccc;padding:10px;background:#f9f9f9;'>", unsafe_allow_html=True)
    for msg in st.session_state.conversation_history:
        if msg.startswith("User:"):
            st.markdown(f"<div style='text-align:right;color:green'><b>{msg}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left;color:#333'><b>{msg}</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# === 🚀 Main App ===
def main():
    st.markdown("<h1 style='text-align:center;'>🌐 Multilingual AI Voice Assistant</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        input_lang_name = st.selectbox("🌍 Input Language:", list(LANGUAGE_MAP.keys()))
    with col2:
        output_lang_name = st.selectbox("🌍 Output Language:", list(LANGUAGE_MAP.keys()))
    input_lang = LANGUAGE_MAP[input_lang_name]
    output_lang = LANGUAGE_MAP[output_lang_name]

    display_chat()

    input_method = st.radio("Input Method:", ["Voice", "Text"])
    user_text = None

    if input_method == "Voice":
        webrtc_streamer(
            key="audio",
            mode=WebRtcMode.SENDONLY,
            audio_processor_factory=AudioProcessor,
            media_stream_constraints={"audio": True, "video": False},
        )
        if st.button("Process Voice Input"):
            user_text = capture_audio_from_queue()
    else:
        user_text = st.text_input("✍️ Type your message:")
        if st.button("Send") and not user_text.strip():
            st.warning("Please enter something!")

    if user_text:
        with st.spinner("Thinking..."):
            ai_response = generate_ai_response(user_text)

        if ai_response:
            st.markdown(f"**🤖 AI:** {ai_response}")
            audio_file = text_to_speech(ai_response, lang=output_lang)
            if audio_file:
                with open(audio_file, "rb") as audio:
                    st.audio(audio, format="audio/mp3")
                    st.download_button("📥 Download", data=audio, file_name="response.mp3")

# Run
if __name__ == "__main__":
    main()
