# Speech-to-Speech Streaming

![Speech-to-Speech Streaming](https://img.shields.io/badge/Language-Python-blue.svg) ![Status](https://img.shields.io/badge/Status-Active-green.svg) ![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📌 Overview
Speech-to-Speech Streaming is an AI-powered application that translates the audio from a video into multiple languages in real-time. Users can upload a video, select a target language, and receive a translated version of the video with speech in the chosen language.

## ✨ Features
- 🎙 Converts speech from video into text using OpenAI Whisper.
- 🌍 Supports translation into 12 languages using LangChain.
- 🔄 Streams the translated speech back into the video.
- 🎥 User-friendly web interface for easy interaction.
- ⚡ Fast processing using FFmpeg for audio extraction.

## 🚀 Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask
- **Machine Learning Models:** OpenAI Whisper, LangChain
- **Others:** FFmpeg, Python, NLP, Deep Learning

## 📂 Project Structure
```
Speech-to-Speech-Streaming/
│── static/              # Static files (CSS, JS, images)
│── templates/           # HTML templates
│── Main.py              # Core logic for speech processing
│── app.py               # Flask application
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
```

## 🔧 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Akshitagupta299/Speech-to-Speech-Streaming.git
cd Speech-to-Speech-Streaming
```

### 2️⃣ Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv myenv
source myenv/bin/activate  # For Linux/Mac
myenv\Scripts\activate     # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Install FFmpeg (Required for Audio Processing)
Ensure FFmpeg is installed and added to the system PATH.
```bash
ffmpeg -version  # Verify installation
```

### 5️⃣ Run the Application
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000/`.

## 🖥️ Usage
1. Upload a video file.
2. Select the target language.
3. Click "Process Video" to start translation.
4. Download or stream the translated video.

## 🛠 Troubleshooting
- **FFmpeg not found?** Ensure it's installed and added to the system PATH.
- **Python 3.12 issues?** Use Python 3.7–3.10 for better compatibility.
- **Whisper import error?** Uninstall `whisper` and install `openai-whisper`.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📬 Contact
For queries or suggestions, reach out to **Akshita Gupta** via [GitHub](https://github.com/Akshitagupta299).

---
Made with ❤️ by **Akshita Gupta**

