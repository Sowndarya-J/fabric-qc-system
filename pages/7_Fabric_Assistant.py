import io
import re
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

mic_error = ""
speech_error = ""
tts_error = ""

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

# ---------------- SESSION ---------------- #
if "fabric_chat" not in st.session_state:
    st.session_state.fabric_chat = []

if "assistant_voice_enabled" not in st.session_state:
    st.session_state.assistant_voice_enabled = False

if "last_spoken_hash" not in st.session_state:
    st.session_state.last_spoken_hash = ""


# ---------------- KNOWLEDGE BASE ---------------- #
FABRIC_KNOWLEDGE = {
    "oil stain": {
        "title": "Oil Stain Defect",
        "what": "Oil stain is a fabric defect where oily marks appear on the cloth surface.",
        "causes": [
            "Machine oil leakage",
            "Improper lubrication control",
            "Dirty rollers or guides",
            "Operator handling with oily hands",
        ],
        "prevention": [
            "Check lubrication system regularly",
            "Clean machine parts and fabric path",
            "Avoid over-oiling",
            "Maintain rollers and moving parts",
        ],
    },
    "hole": {
        "title": "Hole Defect",
        "what": "Hole defect means a visible opening or puncture in the fabric.",
        "causes": [
            "Needle damage",
            "Sharp machine parts",
            "Excess fabric tension",
            "Mechanical puncture during handling",
        ],
        "prevention": [
            "Inspect needles and guides",
            "Reduce damage from sharp edges",
            "Control tension properly",
            "Handle fabric carefully during inspection and transport",
        ],
    },
    "crack": {
        "title": "Crack Defect",
        "what": "Crack defect appears as a broken or damaged line/area in the fabric structure.",
        "causes": [
            "High tension during production",
            "Poor yarn quality",
            "Mechanical stress",
            "Improper handling",
        ],
        "prevention": [
            "Maintain correct tension settings",
            "Use good yarn quality",
            "Check machine movement and pressure",
            "Improve handling process",
        ],
    },
    "knot": {
        "title": "Knot Defect",
        "what": "Knot defect occurs when yarn joints or tied portions become visible on the fabric.",
        "causes": [
            "Improper yarn joining",
            "Frequent yarn breakage",
            "Poor yarn preparation",
        ],
        "prevention": [
            "Improve yarn joining quality",
            "Reduce yarn breaks",
            "Use proper threading and winding",
        ],
    },
    "slub": {
        "title": "Slub Defect",
        "what": "Slub is a thick uneven place in the yarn that appears as a defect in fabric.",
        "causes": [
            "Irregular spinning",
            "Low yarn quality",
            "Improper raw material blending",
        ],
        "prevention": [
            "Improve spinning quality",
            "Use uniform raw materials",
            "Check yarn before fabric production",
        ],
    },
    "broken yarn": {
        "title": "Broken Yarn Defect",
        "what": "Broken yarn defect happens when warp or weft yarn breaks during fabric formation.",
        "causes": [
            "High yarn tension",
            "Weak yarn strength",
            "Needle or guide friction",
            "Machine setting issues",
        ],
        "prevention": [
            "Reduce yarn tension",
            "Use stronger yarn",
            "Inspect yarn path",
            "Maintain machine settings correctly",
        ],
    },
    "warp": {
        "title": "Warp",
        "what": "Warp refers to the lengthwise yarns in the fabric.",
        "causes": [],
        "prevention": [],
    },
    "weft": {
        "title": "Weft",
        "what": "Weft refers to the crosswise yarns inserted across the warp yarns.",
        "causes": [],
        "prevention": [],
    },
    "gsm": {
        "title": "GSM",
        "what": "GSM means grams per square meter. It shows fabric weight and density.",
        "causes": [],
        "prevention": [],
    },
    "quality control": {
        "title": "Fabric Quality Control",
        "what": "Fabric quality control is the process of checking the fabric for defects, consistency, and standards before delivery or use.",
        "causes": [],
        "prevention": [],
    },
    "yolo": {
        "title": "YOLO in Your Project",
        "what": "YOLO is an object detection model. In your project it detects fabric defects from images or camera frames and draws bounding boxes around defect areas.",
        "causes": [],
        "prevention": [],
    },
    "confidence threshold": {
        "title": "Confidence Threshold",
        "what": "Confidence threshold is the minimum score required for the model to show a detection. Higher threshold reduces wrong detections but may miss some weak defects.",
        "causes": [],
        "prevention": [],
    },
    "severity score": {
        "title": "Severity Score",
        "what": "Severity score represents how serious the detected defects are. It is calculated using total defects, high severity defects, and confidence values.",
        "causes": [],
        "prevention": [],
    },
    "project": {
        "title": "Fabric Defect Detection Project",
        "what": "This project is an AI-based Fabric Defect Detection and Quality Control System. It detects defects from uploaded images or webcam capture, shows results, saves inspection history, generates reports, and provides analytics.",
        "causes": [],
        "prevention": [],
    },
    "admin dashboard": {
        "title": "Admin Dashboard",
        "what": "The Admin Dashboard is used to view inspection history, filter records, preview saved images, download CSV, and analyze defects using charts and metrics.",
        "causes": [],
        "prevention": [],
    },
    "image upload": {
        "title": "Image Upload Module",
        "what": "In Image Upload, the user uploads a fabric image, the model detects defects, displays results, shows quality status, and can generate a PDF report.",
        "causes": [],
        "prevention": [],
    },
    "webcam": {
        "title": "Webcam Module",
        "what": "In Live Webcam, the user captures a frame using mobile or webcam, runs detection, sees defect results, and saves the inspection.",
        "causes": [],
        "prevention": [],
    },
}

COMMON_FAQS = {
    "what is this project": "This is an AI-based Fabric Defect Detection and Quality Control System. It uses a YOLO model to detect defects from images and webcam capture, provides quality status, stores history, and supports reports and analytics.",
    "how does this project work": "The project takes a fabric image or webcam frame, runs YOLO defect detection, shows bounding boxes and defect counts, calculates quality status, saves inspection history, and can generate PDF reports.",
    "how to use on mobile": "Open the app in your phone browser, go to the webcam page, allow camera permission, capture a frame, detect defects, and save the result.",
    "what is pass reject": "PASS means the fabric is acceptable based on current logic. REJECT means either a high severity defect is found or total defects exceed the allowed limit.",
    "how to reduce reject rate": "Reduce reject rate by improving yarn quality, controlling machine tension, checking lubrication, cleaning machine parts, and performing regular inspection.",
    "what are common fabric defects": "Common fabric defects include oil stain, hole, crack, knot, slub, broken yarn, warp issues, and weft-related faults.",
}


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


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def format_defect_answer(item: dict) -> str:
    answer = f"**{item['title']}**\n\n{item['what']}"
    if item["causes"]:
        answer += "\n\n**Common causes:**\n" + "\n".join([f"- {x}" for x in item["causes"]])
    if item["prevention"]:
        answer += "\n\n**Prevention / solution:**\n" + "\n".join([f"- {x}" for x in item["prevention"]])
    return answer


def get_free_assistant_answer(question: str) -> str:
    q = normalize_text(question)

    if q in COMMON_FAQS:
        return COMMON_FAQS[q]

    for key, value in COMMON_FAQS.items():
        if key in q:
            return value

    for key, item in FABRIC_KNOWLEDGE.items():
        if key in q:
            return format_defect_answer(item)

    if "difference between warp and weft" in q:
        return (
            "**Warp vs Weft**\n\n"
            "- **Warp**: lengthwise yarns in fabric\n"
            "- **Weft**: crosswise yarns in fabric\n\n"
            "Together they form the woven fabric structure."
        )

    if "confidence threshold" in q:
        return format_defect_answer(FABRIC_KNOWLEDGE["confidence threshold"])

    if "severity score" in q:
        return format_defect_answer(FABRIC_KNOWLEDGE["severity score"])

    if "gpt" in q or "chatgpt" in q:
        return (
            "This Fabric Assistant is a free rule-based assistant for your project. "
            "It answers common textile and fabric defect questions without needing a paid API."
        )

    return (
        "I can help with fabric defects, textile quality control, GSM, warp, weft, "
        "image upload module, webcam module, admin dashboard, and your project explanation. "
        "Try asking things like:\n\n"
        "- What is oil stain defect?\n"
        "- What causes hole defects?\n"
        "- What is GSM in fabric?\n"
        "- How does this project work?\n"
        "- What is warp and weft?"
    )


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
                Free fabric expert assistant for textile defects, quality control, GSM, warp, weft, and your project.
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
    st.session_state.quick_question = "How does this project work?"

# ---------------- VOICE TOGGLE ---------------- #
top_left, top_right = st.columns([4, 1])
with top_left:
    st.caption("Free ChatGPT-style fabric assistant")
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
                <div>Hello! Ask me anything about fabric defects, textile manufacturing, quality control, GSM, warp, weft, or your project.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- INPUT AREA ---------------- #
typed_question = st.text_area(
    "Message",
    height=90,
    label_visibility="collapsed",
    placeholder="Message Fabric Assistant..."
)

c1, c2, c3 = st.columns([1, 1, 2])

with c1:
    send_clicked = st.button("Send", use_container_width=True)

with c2:
    clear_clicked = st.button("Clear Chat", use_container_width=True)

with c3:
    st.caption("Press Send after typing or using voice input.")

if clear_clicked:
    st.session_state.fabric_chat = []
    st.session_state.last_spoken_hash = ""
    if "quick_question" in st.session_state:
        del st.session_state.quick_question
    st.rerun()

question = ""
if typed_question.strip():
    question = typed_question.strip()
elif voice_question.strip():
    question = voice_question.strip()
elif st.session_state.get("quick_question"):
    question = st.session_state.get("quick_question", "").strip()

if send_clicked:
    if not question:
        st.warning("Please type or speak a question first.")
    else:
        st.session_state.fabric_chat.append({"role": "user", "content": question})
        answer = get_free_assistant_answer(question)
        st.session_state.fabric_chat.append({"role": "assistant", "content": answer})
        st.session_state.last_spoken_hash = ""
        if "quick_question" in st.session_state:
            del st.session_state.quick_question
        st.rerun()

if st.session_state.fabric_chat:
    last_msg = st.session_state.fabric_chat[-1]
    if last_msg["role"] == "assistant" and st.session_state.assistant_voice_enabled:
        speak_text_once(last_msg["content"])

st.markdown("</div>", unsafe_allow_html=True)
