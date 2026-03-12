import io
import streamlit as st

from theme import apply_dark_theme

apply_dark_theme()

st.title("🤖 Fabric Assistant")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# Safe imports
try:
    import speech_recognition as sr
except Exception as e:
    sr = None
    sr_error = str(e)
else:
    sr_error = None

try:
    from mic_recorder import mic_recorder
except Exception as e:
    mic_recorder = None
    mic_error = str(e)
else:
    mic_error = None

try:
    from streamlit_chat import message
except Exception as e:
    message = None
    chat_error = str(e)
else:
    chat_error = None

try:
    from gtts import gTTS
except Exception as e:
    gTTS = None
    gtts_error = str(e)
else:
    gtts_error = None

try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None
    openai_error = str(e)
else:
    openai_error = None

# Basic diagnostics
with st.expander("Assistant diagnostics", expanded=False):
    st.write("speech_recognition:", "OK" if sr else f"FAILED - {sr_error}")
    st.write("mic_recorder:", "OK" if mic_recorder else f"FAILED - {mic_error}")
    st.write("streamlit_chat:", "OK" if message else f"FAILED - {chat_error}")
    st.write("gTTS:", "OK" if gTTS else f"FAILED - {gtts_error}")
    st.write("openai:", "OK" if OpenAI else f"FAILED - {openai_error}")
    st.write("OPENAI_API_KEY in secrets:", "YES" if "OPENAI_API_KEY" in st.secrets else "NO")

if OpenAI is None:
    st.error("OpenAI package is not available. Check requirements.txt.")
    st.stop()

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY is missing in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "fabric_chat" not in st.session_state:
    st.session_state.fabric_chat = []

if "assistant_voice_enabled" not in st.session_state:
    st.session_state.assistant_voice_enabled = True

SYSTEM_PROMPT = """
You are a helpful textile and fabric quality control expert assistant.

You answer questions about:
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

Explain clearly and simply.
If asked about a defect, explain:
1. what it is
2. common causes
3. prevention or solution
Keep answers practical and relevant to textile and fabric topics.
"""

def speech_to_text(audio_bytes: bytes) -> str:
    if sr is None:
        raise RuntimeError("SpeechRecognition is not installed properly.")
    recognizer = sr.Recognizer()
    with io.BytesIO(audio_bytes) as wav_io:
        with sr.AudioFile(wav_io) as source:
            audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def speak_text(text: str) -> None:
    if gTTS is None:
        st.warning("Voice reply is unavailable because gTTS failed to load.")
        return
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

voice_question = ""

if mic_recorder is None:
    st.warning("Voice recorder is unavailable. You can still use text chat.")
else:
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
        if message is not None:
            if chat["role"] == "user":
                message(chat["content"], is_user=True, key=f"user_{i}")
            else:
                message(chat["content"], key=f"assistant_{i}")
        else:
            speaker = "You" if chat["role"] == "user" else "Assistant"
            st.markdown(f"**{speaker}:** {chat['content']}")

    last_msg = st.session_state.fabric_chat[-1]
    if last_msg["role"] == "assistant" and st.session_state.assistant_voice_enabled:
        speak_text(last_msg["content"])
