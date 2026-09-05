# 🎙️ Voice Notes → Action Items

An AI-powered application that converts voice recordings into useful, structured information. The application uses **Whisper** for speech-to-text transcription and **Google Gemini** to generate a concise summary, identify actionable tasks, extract deadlines, and identify responsibilities when explicitly mentioned.

## 📌 Project Overview

Voice notes often contain important tasks, dates, decisions, and instructions, but manually reviewing them can be time-consuming.

This project provides a simple Streamlit-based interface where users can upload a voice recording. The application:

1. Converts the voice recording into text using Whisper.
2. Analyzes the transcript using Google Gemini.
3. Generates a concise summary.
4. Extracts actionable tasks.
5. Identifies deadlines when explicitly mentioned.
6. Extracts other important information.
7. Identifies people and responsibilities only when explicitly stated.

The system is designed to avoid inventing deadlines, people, or responsibilities that are not present in the transcript.

## ✨ Features

* 🎤 Voice recording upload
* 📝 Automatic speech-to-text transcription
* 🤖 AI-powered transcript analysis
* 📋 Concise summaries
* ✅ Action-item extraction
* ⏰ Deadline extraction
* 📌 Important information extraction
* 👤 People and responsibility identification
* ⚠️ Unclear speech detection
* 🔐 API key stored securely using `.env`
* 🧹 Automatic cleanup of temporary audio files
* 🎧 Supports MP3, WAV, M4A, and OGG files
* ❌ User-friendly error handling

## 🛠️ Technologies Used

| Technology     | Purpose                                  |
| -------------- | ---------------------------------------- |
| Python         | Application development                  |
| Streamlit      | Web interface                            |
| OpenAI Whisper | Speech-to-text transcription             |
| Google Gemini  | Summarization and action-item extraction |
| python-dotenv  | Environment variable management          |
| FFmpeg         | Audio processing for Whisper             |

## 🔄 System Workflow

```text
Voice Recording
       ↓
Streamlit File Upload
       ↓
Temporary Audio File
       ↓
Whisper Speech-to-Text
       ↓
Transcript
       ↓
Speech Quality Check
       ↓
Google Gemini
       ↓
AI Analysis
       ↓
┌───────────────────────────────┐
│ Summary                       │
│ Action Items                  │
│ Deadlines                     │
│ Important Information         │
│ People / Responsibilities     │
└───────────────────────────────┘
```

## 📁 Project Structure

```text
voice-notes-action-items/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
└── venv/
```

> `.env` and `venv/` are excluded from Git using `.gitignore`.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shrutimahale24-wq/voice-notes-action-items
cd voice-notes-action-items
```

### 2. Create a virtual environment

```bash
py -m venv venv
```

Activate it on Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

Whisper requires FFmpeg for processing audio files.

Make sure FFmpeg is installed and available in the system PATH.

### 5. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not share or commit your API key.

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in the browser.

Upload a supported voice recording and wait for the transcription and AI analysis to complete.

## 🧪 Testing

The application was tested with multiple scenarios.

| Test Case              | Expected Behavior                        | Result   |
| ---------------------- | ---------------------------------------- | -------- |
| No audio uploaded      | Application waits for an upload          | ✅ Passed |
| Unsupported file       | File is rejected by uploader             | ✅ Passed |
| Clear audio            | Transcript and AI analysis generated     | ✅ Passed |
| Unclear/noisy audio    | Warning displayed and processing stopped | ✅ Passed |
| Empty transcript       | User is asked to upload clearer audio    | ✅ Passed |
| Missing Gemini API key | Error message displayed                  | ✅ Passed |
| Gemini API failure     | Graceful error message displayed         | ✅ Passed |

Additional testing included audio containing dates and events to verify that the model does not incorrectly treat general dates as task deadlines.

## 🧠 Prompt Design

The Gemini prompt instructs the model to return five structured sections:

* Summary
* Action Items
* Deadlines
* Important Information
* People / Responsibilities

The prompt also includes explicit constraints such as:

* Do not invent information.
* Do not invent deadlines.
* Do not invent people or responsibilities.
* Do not assume who is responsible for a task.
* Only use information present in the transcript.

These instructions help reduce hallucinated action items and deadlines.

## ⚠️ Error Handling

The application handles several possible failures:

### Missing API Key

If `GEMINI_API_KEY` is not available, the application displays an error and stops.

### Transcription Failure

If Whisper cannot process the uploaded audio, the application displays an error and asks the user to try another file.

### Empty or Unclear Speech

If no meaningful transcript is produced or the speech appears unreliable, the application warns the user instead of sending unreliable content for further analysis.

### Gemini API Failure

If the Gemini request fails, the application displays a user-friendly error instead of crashing.

## ⚠️ Limitations

* Whisper transcription accuracy can decrease with heavy background noise or unclear speech.
* Processing time depends on the audio length and the computer's hardware.
* The application currently processes one uploaded voice note at a time.
* AI-generated results depend on the quality of the transcript.
* The application does not invent missing deadlines or responsibilities; information not explicitly mentioned is reported as not specified.

## 🔒 Security

The Gemini API key is stored in a `.env` file and excluded from Git using `.gitignore`.

The API key should never be committed to the repository or shared publicly.

## 🚀 Future Improvements

Possible future improvements include:

* Batch processing of multiple voice notes
* Exporting results as PDF or text
* Downloadable action-item reports
* Improved structured output using JSON
* Support for additional languages
* Deployment as a public web application

## 👩‍💻 Author

Developed as a take-home assessment project demonstrating speech-to-text processing, LLM-based information extraction, prompt engineering, error handling, and Streamlit application development.
