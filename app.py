import streamlit as st
import whisper
from google import genai
from dotenv import load_dotenv
import os
import tempfile


# -------------------------
# Load Environment Variables
# -------------------------

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


# -------------------------
# Gemini API Key Check
# -------------------------

if not gemini_api_key:

    st.error(
        "⚠️ Gemini API key is missing. "
        "Please add GEMINI_API_KEY to your .env file."
    )

    st.stop()


# -------------------------
# Gemini Client
# -------------------------

client = genai.Client(api_key=gemini_api_key)


# -------------------------
# Load Whisper Model Only Once
# -------------------------

@st.cache_resource
def load_whisper_model():

    return whisper.load_model("base")


model = load_whisper_model()


# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.header("🎙️ About the App")

    st.write(
        "Voice Notes → Action Items converts voice recordings "
        "into useful, structured information using AI."
    )

    st.subheader("✨ What it does")

    st.write("🎤 Converts speech into text")
    st.write("📝 Creates a concise summary")
    st.write("✅ Extracts action items")
    st.write("⏰ Identifies deadlines")
    st.write("📌 Extracts important information")
    st.write("👤 Identifies responsibilities when mentioned")

    st.subheader("🛠️ Technologies")

    st.write("• Python")
    st.write("• Streamlit")
    st.write("• Whisper")
    st.write("• Google Gemini")

    st.subheader("🎧 Supported Formats")

    st.write("MP3 • WAV • M4A • OGG")


# -------------------------
# Page Header
# -------------------------

st.title("🎙️ Voice Notes → Action Items")

st.subheader(
    "Turn your voice notes into clear, actionable information."
)

st.write(
    "Upload a voice recording and let AI transcribe it, "
    "summarize the content, and extract action items, deadlines, "
    "and important information."
)


# -------------------------
# Upload Audio
# -------------------------

audio_file = st.file_uploader(
    "Upload your voice note",
    type=["mp3", "wav", "m4a", "ogg"]
)


if audio_file:

    # -------------------------
    # Play Audio
    # -------------------------

    st.subheader("🎧 Your Voice Note")

    st.audio(audio_file)

    suffix = os.path.splitext(audio_file.name)[1]

    temp_path = None


    # -------------------------
    # Speech-to-Text
    # -------------------------

    with st.spinner("🎤 Transcribing audio..."):

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(audio_file.getbuffer())
                temp_path = temp_file.name

            result = model.transcribe(temp_path)

            transcript = result["text"].strip()

        except Exception:

            st.error(
                "Unable to transcribe the audio. "
                "Please try another audio file."
            )

            st.stop()

        finally:

            if temp_path and os.path.exists(temp_path):

                os.remove(temp_path)


    # -------------------------
    # Empty Transcript Check
    # -------------------------

    if not transcript:

        st.warning(
            "No clear speech was detected. "
            "Please upload a clearer voice recording."
        )

        st.stop()


    # -------------------------
    # Display Transcript
    # -------------------------

    st.subheader("📝 Transcript")

    with st.container(border=True):

        st.write(transcript)


    # -------------------------
    # Speech Quality Check
    # -------------------------

    segments = result.get("segments", [])

    if segments:

        avg_logprob = sum(
            segment["avg_logprob"]
            for segment in segments
        ) / len(segments)

        if avg_logprob < -1.0:

            st.warning(
                "The speech in this recording may be unclear. "
                "Please upload a clearer voice recording."
            )

            st.stop()


    # -------------------------
    # Gemini AI Analysis
    # -------------------------

    st.subheader("🤖 AI Analysis")

    with st.spinner(
        "✨ Generating summary and action items..."
    ):

        try:

            response = client.models.generate_content(

                model="gemini-3.5-flash-lite",

                contents=f"""
You are an assistant that analyzes voice notes.

Analyze the following transcript and extract the meaningful information.

Return the answer using exactly these five sections:

SUMMARY:
Write a concise summary in 1-2 sentences.

ACTION ITEMS:
List each task that someone needs to do as a separate bullet point.
If there are no actionable tasks, write "None identified".

DEADLINES:
For each action item, mention its deadline if the transcript clearly gives one.
If no deadline is mentioned for an action item, write "Not specified".
Do not treat a general date or event as a deadline unless it is connected to a task.
If there are no action items, write "Not specified".

IMPORTANT INFORMATION:
Include other meaningful information from the transcript that is not an action item or deadline.
This may include dates, times, events, decisions, locations, instructions, or other useful facts.
If there is no additional important information, write "None identified".

PEOPLE / RESPONSIBILITIES:
Mention a person's responsibility only if the transcript clearly assigns a task or responsibility to that person.
If no responsibility is explicitly mentioned, write "Not specified".

IMPORTANT RULES:
- Do not invent information.
- Do not invent deadlines.
- Do not invent people or responsibilities.
- Do not assume who is responsible for a task.
- Do not omit meaningful information simply because it is not an action item.
- Keep the response concise.
- Base everything only on the transcript.

Transcript:
{transcript}
"""
            )

            analysis = response.text


            # -------------------------
            # Parse AI Response
            # -------------------------

            sections = {

                "SUMMARY:": "📝 Summary",

                "ACTION ITEMS:": "✅ Action Items",

                "DEADLINES:": "⏰ Deadlines",

                "IMPORTANT INFORMATION:": "📌 Important Information",

                "PEOPLE / RESPONSIBILITIES:":
                    "👤 People / Responsibilities"
            }


            current_section = None

            section_content = {}


            for line in analysis.splitlines():

                line = line.strip()

                if line in sections:

                    current_section = line

                    section_content[current_section] = []

                elif current_section:

                    if line:

                        section_content[
                            current_section
                        ].append(line)


            # -------------------------
            # Display AI Results
            # -------------------------

            for section_key, section_title in sections.items():

                content = section_content.get(
                    section_key,
                    []
                )

                st.markdown(
                    f"### {section_title}"
                )

                with st.container(border=True):

                    if content:

                        for item in content:

                            st.markdown(item)

                    else:

                        st.write("Not specified")


        except Exception:

            st.error(
                "Unable to generate AI analysis right now. "
                "Please try again later."
            )