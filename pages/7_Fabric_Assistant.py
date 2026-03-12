import io
import streamlit as st
import speech_recognition as sr
from mic_recorder import mic_recorder
from streamlit_chat import message
from gtts import gTTS
from openai import OpenAI

from theme import apply_dark_theme

apply_dark_theme()

st.title("🤖 Fabric Assistant")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

if "fabric_chat" not in st.session_state:
    st.session_state.fabric_chat = []

if "assistant_voice_enabled" not in st.session_state:
    st.session_state.assistant_voice_enabled = True

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are a helpful textile and fabric quality control expert assistant.

Your job is to answer questions about:
- fabric defects
- textile manufacturing
- weaving defects
- knitting defects
- dyeing defects
- fabric inspection
- textile quality control
- GSM, yarn count, warp, weft
- AI-based fabric defect detection
- industrial recommendations for defects
- operator guidance and troubleshooting

Rules:
- Explain clearly and simply.
- Answer like a textile expert but make it easy for students and operators.
- If the user asks about a fabric defect, explain:
  1. what it is
  2. common causes
  3. prevention or solution
- If the user asks about the project, explain it as an AI-based Fabric Defect Detection and Quality Control System.
- Keep answers practical and relevant to textile/fabric topics.
"""


def speech_to_text(audio_bytes: bytes) -> str:
    recognizer = sr.Recognizer()
    with io.BytesIO(audio_bytes) as wav_io:
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)
    return recognizer.recognize_google(audio)


def speak_text(text: str) -> None:
    tts = gTTS(text=text, lang="en")
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp.read(), format="audio/mp3")


st.markdown(
    """
    <div class="soft-box">
        <b>Ask anything about fabrics, textile defects, quality control, or your project.</b><br><br>
        Example questions:<br>
        • What is oil stain defect?<br>
        • What causes hole defects in fabric?<br>
        • What is warp and weft?<br>
        • How does this project work?<br>
        • How to reduce reject rate in fabric inspection?<br>
        • What is GSM in fabric?
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns([3, 1])
with c1:
    typed_question = st.text_input("Type your question")
with c2:
    st.toggle("Voice Reply", key="assistant_voice_enabled")

st.subheader("🎤 Voice Input")

audio = mic_recorder(
    start_prompt="Start Talking",
    stop_prompt="Stop Recording",
    just_once=True,
    use_container_width=True,
    key="fabric_assistant_mic",
)

voice_question = ""

if audio:
    try:
        voice_question = speech_to_text(audio["bytes"])
        st.success("Voice recognized successfully")
        st.text_area("Recognized Speech", value=voice_question, height=100)
    except Exception as e:
        st.error(f"Voice recognition failed: {e}")

question = typed_question.strip() if typed_question.strip() else voice_question.strip()

col_ask, col_clear = st.columns(2)

with col_ask:
    ask_clicked = st.button("Ask Assistant", use_container_width=True)

with col_clear:
    clear_clicked = st.button("Clear Chat", use_container_width=True)

if clear_clicked:
    st.session_state.fabric_chat = []
    st.rerun()

if ask_clicked:
    if not question:
        st.warning("Please type or speak a question first.")
    else:
        st.session_state.fabric_chat.append({"role": "user", "content": question})

        messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.fabric_chat

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_api,
                temperature=0.4,
            )

            answer = response.choices[0].message.content.strip()

            st.session_state.fabric_chat.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Assistant error: {e}")

if st.session_state.fabric_chat:
    st.subheader("💬 Chat")

    for i, chat in enumerate(st.session_state.fabric_chat):
        if chat["role"] == "user":
            message(chat["content"], is_user=True, key=f"user_{i}")
        else:
            message(chat["content"], key=f"assistant_{i}")

    last_msg = st.session_state.fabric_chat[-1]
    if (
        last_msg["role"] == "assistant"
        and st.session_state.assistant_voice_enabled
    ):
        speak_text(last_msg["content"])
