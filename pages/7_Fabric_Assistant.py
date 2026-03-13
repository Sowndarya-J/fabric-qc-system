import io
import hashlib
import streamlit as st

from theme import apply_dark_theme

apply_dark_theme()

st.title("🤖 Fabric Assistant")

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# ---------------- SAFE IMPORTS ---------------- #
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

# ---------------- API CHECK ---------------- #
if not openai_ok:
    st.error(f"OpenAI package import failed: {openai_error}")
    st.stop()

if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY is missing in Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SESSION ---------------- #
if "fabric_chat" not in st.session_state:
    st.session_state.fabric_chat = []

if "assistant_voice_enabled" not in st.session_state:
    st.session_state.assistant_voice_enabled = False

if "last_spoken_hash" not in st.session_state:
    st.session_state.last_spoken_hash = ""

# ---------------- SYSTEM PROMPT ---------------- #
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

Rules:
- Explain clearly and simply.
- If asked about a defect, explain:
  1. what it is
  2. common causes
  3. prevention or solution
- Keep answers practical and relevant to textile and fabric topics.
- Keep answers concise but useful.
"""

# ---------------- HELPERS ---------------- #
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


def ask_openai(question: str) -> str:
    messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.fabric_chat
    messages_for_api.append({"role": "user", "content": question})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for_api,
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()

# ---------------- PAGE CSS ---------------- #
st.markdown("""
<style>
.chatgpt-shell {
    max-width: 950px;
    margin: 0 auto;
}

.chatgpt-topbox {
    background: #161616;
    border: 1px solid #2d2d2d;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
}

.chat-scroll-box {
    background: #0f0f0f;
    border: 1px solid #222;
    border-radius: 16px;
    padding: 12px;
    min-height: 420px;
    max-height: 520px;
    overflow-y: auto;
}

.user-bubble {
    background: #1f1f1f;
    border: 1px solid #333;
    border-radius: 16px;
    padding: 14px 16px;
    margin: 10px 0 10px auto;
    width: fit-content;
    max-width: 80%;
}

.assistant-row {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin: 14px 0;
}

.assistant-avatar {
    min-width: 38px;
    height: 38px;
    border-radius: 10px;
    background: #ff3b3b;
    color: white !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 18px;
}

.assistant-bubble {
    background: #161616;
    border: 1px solid #2d2d2d;
    border-radius: 16px;
    padding: 14px 16px;
    width: 100%;
}

.assistant-name {
    font-weight: 700;
    color: #ff6b6b !important;
    margin-bottom: 6px;
}

.chat-input-box {
    background: #111111;
    border: 1px solid #2d2d2d;
    border-radius: 18px;
    padding: 10px;
    margin-top: 14px;
}

.small-note {
    color: #c7c7c7 !important;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TOP BOX ---------------- #
st.markdown(
    """
    <div class="chatgpt-shell">
        <div class="chatgpt-topbox">
            <h3 style="margin:0;">Fabric Assistant</h3>
            <p class="small-note" style="margin-top:8px;">
                Ask anything about fabrics, textile defects, quality control, weaving, knitting, GSM, warp, weft, and your project.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- QUICK ACTIONS ---------------- #
q1, q2, q3, q4 = st.columns(4)
if q1.button("What is oil stain defect?", use_container_width=True):
    st.session_state.quick_question = "What is oil stain defect?"
if q2.button("What causes hole defects?", use_container_width=True):
    st.session_state.quick_question = "What causes hole defects in fabric?"
if q3.button("Explain GSM", use_container_width=True):
    st.session_state.quick_question = "What is GSM in fabric?"
if q4.button("How does this project work?", use_container_width=True):
    st.session_state.quick_question = "How does this fabric defect detection project work?"

# ---------------- VOICE TOGGLE ---------------- #
top_left, top_right = st.columns([4, 1])
with top_left:
    st.caption("ChatGPT-style fabric expert assistant")
with top_right:
    st.toggle("Voice Reply", key="assistant_voice_enabled")

# ---------------- VOICE INPUT ---------------- #
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
                st.text_area("Recognized Speech", value=voice_question, height=90)
            except Exception as e:
                st.error(f"Voice recognition failed: {e}")
    else:
        st.info("Voice input is unavailable. Use text chat.")

# ---------------- CHAT HISTORY ---------------- #
st.markdown('<div class="chatgpt-shell">', unsafe_allow_html=True)
st.markdown('<div class="chat-scroll-box">', unsafe_allow_html=True)

if st.session_state.fabric_chat:
    for item in st.session_state.fabric_chat:
        if item["role"] == "user":
            st.markdown(
                f"""
                <div style="display:flex; justify-content:flex-end;">
                    <div class="user-bubble">{item["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="assistant-row">
                    <div class="assistant-avatar">F</div>
                    <div class="assistant-bubble">
                        <div class="assistant-name">Fabric Assistant</div>
                        <div>{item["content"]}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.markdown(
        """
        <div class="assistant-row">
            <div class="assistant-avatar">F</div>
            <div class="assistant-bubble">
                <div class="assistant-name">Fabric Assistant</div>
                <div>Hello! Ask me anything about fabric defects, textile manufacturing, quality control, or your project.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- INPUT AREA ---------------- #
typed_question = st.text_area("Message", height=90, label_visibility="collapsed", placeholder="Message Fabric Assistant...")

c1, c2, c3 = st.columns([1, 1, 2])

with c1:
    send_clicked = st.button("Send", use_container_width=True)

with c2:
    clear_clicked = st.button("Clear Chat", use_container_width=True)

with c3:
    st.caption("Press Send after typing or using voice input.")

# ---------------- CLEAR ---------------- #
if clear_clicked:
    st.session_state.fabric_chat = []
    st.session_state.last_spoken_hash = ""
    if "quick_question" in st.session_state:
        del st.session_state.quick_question
    st.rerun()

# ---------------- FINAL QUESTION ---------------- #
question = ""
if typed_question.strip():
    question = typed_question.strip()
elif voice_question.strip():
    question = voice_question.strip()
elif st.session_state.get("quick_question"):
    question = st.session_state.get("quick_question", "").strip()

# ---------------- SEND ---------------- #
if send_clicked:
    if not question:
        st.warning("Please type or speak a question first.")
    else:
        st.session_state.fabric_chat.append({"role": "user", "content": question})

        try:
            answer = ask_openai(question)
            st.session_state.fabric_chat.append({"role": "assistant", "content": answer})
            st.session_state.last_spoken_hash = ""
            if "quick_question" in st.session_state:
                del st.session_state.quick_question
            st.rerun()
        except Exception as e:
            st.error(f"Assistant error: {e}")

# ---------------- SPEAK LAST ANSWER ---------------- #
if st.session_state.fabric_chat:
    last_msg = st.session_state.fabric_chat[-1]
    if last_msg["role"] == "assistant" and st.session_state.assistant_voice_enabled:
        speak_text_once(last_msg["content"])

st.markdown("</div>", unsafe_allow_html=True)
