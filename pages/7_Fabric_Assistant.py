import streamlit as st
from streamlit_chat import message
from mic_recorder import mic_recorder
import speech_recognition as sr
import io
from gtts import gTTS
from openai import OpenAI

from theme import apply_dark_theme

apply_dark_theme()

st.title("🧠 Fabric AI Assistant")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Chat history
if "fabric_chat" not in st.session_state:
    st.session_state.fabric_chat = []

# AI system role
SYSTEM_PROMPT = """
You are a textile quality control expert.

You help with:
fabric defects
textile manufacturing
quality inspection
weaving defects
knitting defects
dyeing defects
fabric testing
industrial textile production
AI fabric inspection

Explain clearly for students and textile engineers.
"""

# --------------------
# Voice Recognition
# --------------------

def speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    with io.BytesIO(audio_bytes) as wav_io:
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)

    return recognizer.recognize_google(audio)


# --------------------
# Voice Output
# --------------------

def speak(text):

    tts = gTTS(text)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    st.audio(fp.read(), format="audio/mp3")


# --------------------
# Voice Question
# --------------------

st.subheader("🎤 Ask with Voice")

audio = mic_recorder(
    start_prompt="Start Talking",
    stop_prompt="Stop",
    just_once=True,
    use_container_width=True
)

voice_question = ""

if audio:
    try:
        voice_question = speech_to_text(audio["bytes"])
        st.success("Voice recognized")
        st.write("You said:", voice_question)
    except:
        st.error("Voice recognition failed")


# --------------------
# Chat Question
# --------------------

st.subheader("💬 Ask About Fabrics")

text_question = st.text_input("Type your question")

question = text_question if text_question else voice_question


# --------------------
# Ask Assistant
# --------------------

if st.button("Ask Assistant"):

    if question.strip() == "":
        st.warning("Please ask a question")

    else:

        st.session_state.fabric_chat.append(
            {"role": "user", "content": question}
        )

        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.fabric_chat

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        answer = response.choices[0].message.content

        st.session_state.fabric_chat.append(
            {"role": "assistant", "content": answer}
        )

        speak(answer)


# --------------------
# Chat Display
# --------------------

for i, chat in enumerate(st.session_state.fabric_chat):

    if chat["role"] == "user":
        message(chat["content"], is_user=True, key=f"user{i}")

    else:
        message(chat["content"], key=f"bot{i}")


# --------------------
# Fabric Defect Learning
# --------------------

st.divider()
st.header("📚 Fabric Defect Learning")

defect = st.selectbox(
    "Select Defect Type",
    [
        "Hole",
        "Oil Stain",
        "Crack",
        "Knot",
        "Slub",
        "Broken Yarn"
    ]
)

defect_info = {

    "Hole":
    "Hole defects occur when yarn breaks or fabric is damaged during weaving. Causes include needle damage or machine friction.",

    "Oil Stain":
    "Oil stains happen due to lubrication oil leakage from machines. Proper machine maintenance reduces this defect.",

    "Crack":
    "Crack defects appear due to excessive tension during weaving or knitting processes.",

    "Knot":
    "Knots occur when yarn ends are tied together during yarn joining.",

    "Slub":
    "Slub defects are thick yarn segments caused by irregular spinning.",

    "Broken Yarn":
    "Broken yarn defects occur when warp or weft yarn breaks during fabric production."
}

st.info(defect_info[defect])


# --------------------
# Operator Training Assistant
# --------------------

st.divider()
st.header("🏭 Operator Training Assistant")

problem = st.selectbox(
    "Select Fabric Problem",
    [
        "Too many oil stains",
        "Hole defects increasing",
        "Frequent yarn break",
        "High reject rate"
    ]
)

solutions = {

    "Too many oil stains":
    "Check machine lubrication system and reduce oil overflow. Clean rollers regularly.",

    "Hole defects increasing":
    "Inspect needles, machine tension, and yarn strength.",

    "Frequent yarn break":
    "Reduce yarn tension and inspect yarn quality.",

    "High reject rate":
    "Improve fabric inspection process and machine calibration."
}

st.success(solutions[problem])
