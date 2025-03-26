# 🌐 Multilingual Voice-Based AI Assistant

This is a **Multilingual AI Assistant** powered by **Google Gemini AI**. It supports both **voice** and **text-based conversations** in multiple languages, providing a conversational experience with AI-generated responses. The assistant can respond in both **text and speech**.

---
## 🚀 **Try it Live on Hugging Face Spaces**  

Experience the Multilingual AI Assistant directly on Hugging Face Spaces without any setup!  

👉 [**Launch the App on Hugging Face**](https://huggingface.co/spaces/AmritSbisht/Multilingual-Voice-Based-AI-Assistant)

> No installation needed — just click and start chatting! 🌐


## 🚀 **Features**
- **Multilingual Support**: Communicate in various languages like English, Hindi, Spanish, French, German, and Chinese.
- **Voice and Text Input**: Choose to speak using your microphone or type using the text input.
- **AI-Powered Responses**: Get intelligent and conversational responses using **Google Gemini AI**.
- **Speech Output**: AI-generated responses are converted to speech using **gTTS (Google Text-to-Speech)**.
- **Conversation Memory**: Maintains memory of the last 6 interactions for a natural conversational experience.
- **Downloadable Audio**: Download AI-generated audio responses as `.mp3` files.

---

## 🛠 **Tech Stack**
- **Python**: Core programming language.
- **Streamlit**: For building the interactive UI.
- **SpeechRecognition**: For voice input using the microphone.
- **gTTS (Google Text-to-Speech)**: For converting AI responses into speech.
- **Google Gemini AI**: For generating AI responses.
- **Dotenv**: For securely managing API keys.

---

## 🔎 **Setup Instructions**

1. **Clone the Repository**  
    ```bash
    git clone https://github.com/your-repo/multilingual-ai-assistant.git
    cd multilingual-ai-assistant
    ```

2. **Create a Virtual Environment**  
    ```bash
    python -m venv myenv
    source myenv/bin/activate    # On macOS/Linux
    myenv\Scripts\activate        # On Windows
    ```

3. **Install Dependencies**  
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up API Key**  
    - Create a `.env` file in the root directory.  
    - Add your Google API Key using this format:  
    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

5. **Run the App**  
    ```bash
    streamlit run app.py
    ```

---

## 🧑‍💻 **How to Use**

1. Select your **Input Language** and **Output Language** from the dropdown.  
2. Choose your preferred **Input Method**:  
    - **Voice**: Click the **"Start Speaking"** button to speak.  
    - **Text**: Type your message and click the **"Send"** button.  
3. The AI will generate a response in text and speech.  
4. Download the AI response using the **"Download AI Response"** button if needed.  

---

## 🌐 **Supported Languages**
- **English** (en)  
- **Hindi** (hi)  
- **Spanish** (es)  
- **French** (fr)  
- **German** (de)  
- **Chinese** (zh)  

---

## ⚠️ **Troubleshooting**

- **Microphone Not Working?**  
    - Ensure your microphone is properly connected and granted access.  
    - Restart the app and try again.  

- **API Errors?**  
    - Verify your API key in the `.env` file.  
    - Ensure you have access to **Google Gemini AI**.  

- **Speech Not Playing?**  
    - Ensure `gTTS` is installed and operational.  
    - Check for errors in the Streamlit console.  

---

## 💡 **Contributing**

Contributions are welcome!  
1. Fork the repository.  
2. Create your feature branch: `git checkout -b feature/new-feature`.  
3. Commit your changes: `git commit -m 'Add some feature'`.  
4. Push to the branch: `git push origin feature/new-feature`.  
5. Open a Pull Request.  

---

## 📜 **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## ✨ **Acknowledgements**
- **Google Gemini AI** for the AI-powered responses.  
- **gTTS** for speech generation.  
- **SpeechRecognition** for accurate voice input.  
- **Streamlit** for the beautiful and interactive UI.  

---

Enjoy your multilingual AI assistant experience! 🚀
