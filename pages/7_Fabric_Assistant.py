import io
import hashlib
import streamlit as st

from theme import apply_dark_theme

apply_dark_theme()

st.title("🤖 Fabric Assistant")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# Safe imports
mic_ok = True
speech_ok = True
tts_ok = True
openai_ok = True

mic_error = ""
speech_error = ""
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
    from gtts import gTTS
except Exception as e:
    tts_ok = False
    tts_error = str(e)

try:
    from openai import OpenAI
except Exception as e:
    openai_ok = False
    openai_error = str(e)

if not openai_ok:
    st.error(f"OpenAI package import failed: {openai_error}")
    st.stop()

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY is missing in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "fabric_chat" not in st.session_state:
    st.session_state.fabric_chat = []

if "assistant_voice_enabled" not in st.session_state:
    st.session_state.assistant_voice_enabled = True

if "last_spoken_hash" not in st.session_state:
    st.session_state.last_spoken_hash = ""

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
Keep answers concise but useful.
"""

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
    except Exception:
        pass

st.markdown(
    """
    <div class="chat-shell">
        <div class="soft-box chat-title">
            <h3>Ask anything about fabrics, textile defects, quality control, or your project.</h3>
            <p>
                Examples: What is oil stain defect? What causes hole defects?
                What is GSM in fabric? How does this project work?
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

top1, top2 = st.columns([4, 1])
with top1:
    typed_question = st.text_input("Message Fabric Assistant")
with top2:
    st.toggle("Voice Reply", key="assistant_voice_enabled")

voice_question = ""
with st.expander("🎤 Voice Input", expanded=False):
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

c1, c2 = st.columns([1, 1])
with c1:
    ask_clicked = st.button("Send", use_container_width=True)
with c2:
    clear_clicked = st.button("Clear Chat", use_container_width=True)

if clear_clicked:
    st.session_state.fabric_chat = []
    st.session_state.last_spoken_hash = ""
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
            st.session_state.last_spoken_hash = ""
        except Exception as e:
            st.error(f"Assistant error: {e}")

st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

if st.session_state.fabric_chat:
    for i, chat in enumerate(st.session_state.fabric_chat):
        if chat["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-msg-user">
                    <div class="chat-role">You</div>
                    <div>{chat["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="chat-msg-bot">
                    <div class="chat-role">Fabric Assistant</div>
                    <div>{chat["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    last_msg = st.session_state.fabric_chat[-1]
    if last_msg["role"] == "assistant" and st.session_state.assistant_voice_enabled:
        speak_text_once(last_msg["content"])
else:
    st.markdown(
        """
        <div class="soft-box">
            Start chatting with the Fabric Assistant.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
