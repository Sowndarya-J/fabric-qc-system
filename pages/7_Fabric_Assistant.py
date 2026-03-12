import io
import hashlib
import streamlit as st

from theme import apply_dark_theme

apply_dark_theme()

st.title("🤖 Fabric Assistant")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# -----------------------------
# SAFE IMPORTS
# -----------------------------
mic_ok = True
speech_ok = True
chat_ok = True
tts_ok = True
openai_ok = True

mic_error = ""
speech_error = ""
chat_error = ""
tts_error = ""
openai_error = ""

try:
    import speech_recognition as sr
except Exception as e:
    speech_ok = False
    speech_error = str(e)

try:
    from mic_recorder import mic_recorder
except Exception as e:
    mic_ok = False
    mic_error = str(e)

try:
    from streamlit_chat import message
except Exception as e:
    chat_ok = False
    chat_error = str(e)

try:
    from gtts import gTTS
except Exception as e:
    tts_ok = False
    tts_error = str(e)

try:
    from openai import OpenAI
except Exception as e:
    openai_ok = False
    openai_error = str(e)

# -----------------------------
# SECRETS CHECK
# -----------------------------
if not openai_ok:
    st.error(f"OpenAI package import failed: {openai_error}")
    st.stop()

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY is missing in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# SESSION STATE
# -----------------------------
if "fabric_chat" not in st.session_state:
    st.session_state.fabric_chat = []

if "assistant_voice_enabled" not in st.session_state:
    st.session_state.assistant_voice_enabled = True

if "last_spoken_hash" not in st.session_state:
    st.session_state.last_spoken_hash = ""

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
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
- Keep answers concise but useful.
"""

# -----------------------------
# HELPERS
# -----------------------------
def speech_to_text(audio_bytes: bytes) -> str:
    if not speech_ok:
        raise RuntimeError(f"SpeechRecognition not available: {speech_error}")

    recognizer = sr.Recognizer()
    with io.BytesIO(audio_bytes) as wav_io:
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)

    return recognizer.recognize_google(audio)


def speak_text_once(text: str) -> None:
    if not tts_ok:
        st.warning(f"Voice reply unavailable: {tts_error}")
        return

    text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
    if st.session_state.last_spoken_hash == text_hash:
        return

    try:
        tts = gTTS(text=text, lang="en")
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp.read(), format="audio/mp3")
        st.session_state.last_spoken_hash = text_hash
    except Exception as e:
        st.warning(f"Voice reply failed: {e}")


def render_chat_bubble(role: str, content: str, idx: int) -> None:
    if chat_ok:
        if role == "user":
            message(content, is_user=True, key=f"user_{idx}")
        else:
            message(content, key=f"assistant_{idx}")
    else:
        speaker = "You" if role == "user" else "Assistant"
        st.markdown(f"**{speaker}:** {content}")


# -----------------------------
# OPTIONAL DIAGNOSTICS
# -----------------------------
with st.expander("Assistant diagnostics", expanded=False):
    st.write("Mic recorder:", "OK" if mic_ok else f"FAILED - {mic_error}")
    st.write("Speech recognition:", "OK" if speech_ok else f"FAILED - {speech_error}")
    st.write("Chat UI:", "OK" if chat_ok else f"FAILED - {chat_error}")
    st.write("Text-to-speech:", "OK" if tts_ok else f"FAILED - {tts_error}")
    st.write("OpenAI:", "OK" if openai_ok else f"FAILED - {openai_error}")
    st.write("API key found:", "YES")

# -----------------------------
# UI
# -----------------------------
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

voice_question = ""

if mic_ok:
    audio = mic_recorder(
        start_prompt="Start Talking",
        stop_prompt="Stop Recording",
        just_once=True,
        use_container_width=True,
        key="fabric_assistant_mic",
    )

    if audio:
        try:
            voice_question = speech_to_text(audio["bytes"])
            st.success("Voice recognized successfully")
            st.text_area("Recognized Speech", value=voice_question, height=100)
        except Exception as e:
            st.error(f"Voice recognition failed: {e}")
else:
    st.info("Voice input is unavailable. You can still use text chat.")

question = typed_question.strip() if typed_question.strip() else voice_question.strip()

col_ask, col_clear = st.columns(2)

with col_ask:
    ask_clicked = st.button("Ask Assistant", use_container_width=True)

with col_clear:
    clear_clicked = st.button("Clear Chat", use_container_width=True)

if clear_clicked:
    st.session_state.fabric_chat = []
    st.session_state.last_spoken_hash = ""
    st.rerun()

# -----------------------------
# ASK ASSISTANT
# -----------------------------
if ask_clicked:
    if not question:
        st.warning("Please type or speak a question first.")
    else:
        st.session_state.fabric_chat.append(
            {"role": "user", "content": question}
        )

        messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.fabric_chat

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_api,
                temperature=0.4,
            )

            answer = response.choices[0].message.content.strip()

            st.session_state.fabric_chat.append(
                {"role": "assistant", "content": answer}
            )

            # reset spoken hash so new answer can be spoken
            st.session_state.last_spoken_hash = ""

        except Exception as e:
            st.error(f"Assistant error: {e}")

# -----------------------------
# CHAT DISPLAY
# -----------------------------
if st.session_state.fabric_chat:
    st.subheader("💬 Chat")

    for i, chat in enumerate(st.session_state.fabric_chat):
        render_chat_bubble(chat["role"], chat["content"], i)

    last_msg = st.session_state.fabric_chat[-1]
    if last_msg["role"] == "assistant" and st.session_state.assistant_voice_enabled:
        speak_text_once(last_msg["content"])
