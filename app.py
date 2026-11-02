import os
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# Configuration & Environment Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CaseScribe — Multilingual Incident Documentation",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
try:
    from dotenv import load_dotenv
    # Look for .env in current directory or script parent directory
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except Exception:
    pass

# Retrieve API key from environment or Streamlit secrets
def get_sarvam_api_key():
    # 1. Environment variable
    key = os.environ.get("SARVAM_API_KEY")
    if key and key.strip():
        return key.strip()
    # 2. Streamlit secrets
    try:
        if "SARVAM_API_KEY" in st.secrets:
            return st.secrets["SARVAM_API_KEY"].strip()
    except Exception:
        pass
    return None

configured_key = get_sarvam_api_key()

# -----------------------------------------------------------------------------
# Fictional Scenarios & Demo Data
# -----------------------------------------------------------------------------
FICTIONAL_PUNE_SCENARIO_EN = (
    "Yesterday evening, around 7:30 PM, I was near the main gate of a college in Pune. "
    "I saw a person wearing a dark jacket arguing with a delivery rider. A few minutes later, "
    "I heard a loud noise and noticed that the rider had fallen. I did not see exactly what caused the fall. "
    "Another person standing nearby called for help. I left after the ambulance arrived."
)

FICTIONAL_PUNE_SCENARIO_MR = (
    "काल संध्याकाळी सुमारे साडेसातच्या सुमारास मी पुण्यातील एका कॉलेजच्या मुख्य प्रवेशद्वाराजवळ होतो. "
    "काळ्या जॅकेट घातलेली एक व्यक्ती आणि डिलिव्हरी रायडर यांच्यात जोरदार वाद सुरू असलेला मी पाहिला. "
    "काही मिनिटांनंतर मोठा आवाज ऐकू आला आणि रायडर खाली पडल्याचे दिसले. तो कसा पडला हे मी स्पष्ट पाहिले नाही. "
    "जवळ उभ्या असलेल्या एका व्यक्तीने मदतीसाठी हाक मारली. रुग्णवाहिका आल्यावर मी तिथून निघालो."
)

FICTIONAL_PUNE_SCENARIO_HI = (
    "कल शाम करीब 7:30 बजे, मैं पुणे में एक कॉलेज के मुख्य गेट के पास था। "
    "मैंने काले जैकेट पहने एक व्यक्ति को डिलीवरी राइडर से बहस करते देखा। कुछ मिनट बाद, "
    "मुझे एक तेज आवाज सुनाई दी और देखा कि राइडर जमीन पर गिर पड़ा था। मुझे ठीक से दिखाई नहीं दिया कि वह कैसे गिरा। "
    "पास खड़े एक व्यक्ति ने मदद के लिए आवाज लगाई। एम्बुलेंस आने के बाद मैं वहां से चला गया।"
)

PRECOMPUTED_DEMO_REPORT = {
    "incident_summary": (
        "The narrator reports observing an argument between an unidentified person wearing a dark jacket "
        "and a delivery rider near a college main gate in Pune around 7:30 PM. Shortly afterward, a loud noise "
        "was heard, and the delivery rider was found fallen. The narrator notes not having seen what caused the fall. "
        "A bystander requested emergency assistance, and an ambulance subsequently arrived."
    ),
    "reported_events": [
        {
            "event_description": "Narrator was positioned near the main gate of a college in Pune.",
            "date": "Yesterday evening",
            "time": "Around 7:30 PM",
            "location": "Near main gate of college, Pune",
            "people_mentioned": ["Narrator"],
            "source_excerpt": "Yesterday evening, around 7:30 PM, I was near the main gate of a college in Pune."
        },
        {
            "event_description": "Narrator observed a verbal dispute between a person wearing a dark jacket and a delivery rider.",
            "date": "Yesterday evening",
            "time": "Around 7:30 PM",
            "location": "Near main gate of college, Pune",
            "people_mentioned": ["Person in dark jacket", "Delivery rider"],
            "source_excerpt": "I saw a person wearing a dark jacket arguing with a delivery rider."
        },
        {
            "event_description": "Loud noise heard; narrator noticed the delivery rider had fallen onto the ground. Cause of fall was not directly witnessed.",
            "date": "Yesterday evening",
            "time": "A few minutes after 7:30 PM (approximate)",
            "location": "Near main gate of college, Pune",
            "people_mentioned": ["Delivery rider"],
            "source_excerpt": "A few minutes later, I heard a loud noise and noticed that the rider had fallen. I did not see exactly what caused the fall."
        },
        {
            "event_description": "An unidentified nearby bystander summoned help.",
            "date": "Yesterday evening",
            "time": "Not specified",
            "location": "Near main gate of college, Pune",
            "people_mentioned": ["Another person standing nearby (bystander)"],
            "source_excerpt": "Another person standing nearby called for help."
        },
        {
            "event_description": "Emergency medical vehicle (ambulance) arrived at the location.",
            "date": "Yesterday evening",
            "time": "Not specified",
            "location": "Near main gate of college, Pune",
            "people_mentioned": ["Ambulance personnel (implied)"],
            "source_excerpt": "the ambulance arrived"
        },
        {
            "event_description": "Narrator departed from the scene following the ambulance's arrival.",
            "date": "Yesterday evening",
            "time": "Not specified (post-ambulance arrival)",
            "location": "Near main gate of college, Pune",
            "people_mentioned": ["Narrator"],
            "source_excerpt": "I left after the ambulance arrived."
        }
    ],
    "people_mentioned": [
        "Narrator (Observer)",
        "Person wearing a dark jacket",
        "Delivery rider",
        "Bystander standing nearby",
        "Ambulance responders (inferred from vehicle arrival)"
    ],
    "locations_mentioned": [
        "College main gate, Pune"
    ],
    "dates_and_times": [
        "Yesterday evening",
        "Around 7:30 PM",
        "A few minutes later (approximate)"
    ],
    "missing_information": [
        "Exact calendar date of the occurrence (only 'yesterday' reported)",
        "Name or specific campus identification of the college in Pune",
        "Identity, physical description, or vehicle details of the person in the dark jacket",
        "Delivery company or vehicle details (license plate/model) of the delivery rider",
        "Specific origin or nature of the reported loud noise",
        "Contact information or identity of the bystander who called for help",
        "Identity or hospital affiliation of the responding ambulance"
    ],
    "clarification_questions": [
        "What was the specific calendar date on which this incident took place?",
        "Which specific college campus or street in Pune was this located at?",
        "Can you describe the direction from which the loud noise originated?",
        "Did you observe any vehicles or physical contact immediately preceding the fall?",
        "Did the person in the dark jacket remain at the scene when the ambulance arrived or leave in a specific direction?"
    ],
    "potential_inconsistencies": [
        "No direct factual contradictions identified within the narrator's statement.",
        "Crucial chain-of-events ambiguity: The narrator observed an argument and later a fallen rider, but explicitly notes not witnessing the physical cause of the fall. Caution must be exercised to prevent assuming causation."
    ],
    "translated_summary": (
        "पुणे येथील एका महाविद्यालयाच्या मुख्य गेटजवळ काल संध्याकाळी सुमारे ७:३० वाजता काळ्या जॅकेटमधील व्यक्ती "
        "आणि डिलिव्हरी रायडर यांच्यात वाद झाला. थोड्याच वेळात मोठ्या आवाजानंतर रायडर खाली पडल्याचे दिसले. "
        "पडण्याचे थेट कारण पाहिले गेले नाही. एका प्रत्यक्षदर्शीने मदतीस बोलावले व रुग्णवाहिका दाखल झाल्यानंतर निवेदक निघून गेला."
    ),
    "disclaimer": "This is an AI-organized account requiring human review."
}

# -----------------------------------------------------------------------------
# Custom Styling (Dark Navy / Charcoal + Restrained Teal)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* Dark Navy/Charcoal Theme Variables */
    :root {
        --bg-main: #0B0F19;
        --card-bg: #111827;
        --card-border: #1F2937;
        --teal-accent: #0D9488;
        --teal-light: #14B8A6;
        --teal-glow: rgba(20, 184, 166, 0.15);
        --text-primary: #F3F4F6;
        --text-secondary: #9CA3AF;
        --accent-amber: #F59E0B;
        --accent-blue: #38BDF8;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header styling */
    .app-header-box {
        background: linear-gradient(135deg, #0F172A 0%, #111827 100%);
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .app-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .app-tagline {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-top: 6px;
        font-weight: 400;
    }

    .hackathon-badge {
        display: inline-block;
        background: rgba(13, 148, 136, 0.2);
        color: #2DD4BF;
        border: 1px solid rgba(45, 212, 191, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* Persistent Disclaimer Banner */
    .disclaimer-banner {
        background: #181E29;
        border-left: 4px solid #F59E0B;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 20px;
        color: #D1D5DB;
        font-size: 0.88rem;
        line-height: 1.45;
    }

    /* Card Panels */
    .custom-card {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #1F2937;
        padding-bottom: 8px;
    }

    /* Timeline Cards */
    .timeline-item {
        background: #131D2E;
        border: 1px solid #1E293B;
        border-left: 3px solid #14B8A6;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }

    .timeline-time-badge {
        display: inline-block;
        background: #1E293B;
        color: #38BDF8;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.78rem;
        font-family: monospace;
        margin-bottom: 6px;
    }

    .source-quote {
        background: rgba(15, 23, 42, 0.6);
        border-left: 2px solid #64748B;
        padding: 6px 12px;
        margin-top: 8px;
        font-style: italic;
        color: #94A3B8;
        font-size: 0.84rem;
        border-radius: 0 4px 4px 0;
    }

    /* Chips */
    .tag-chip {
        display: inline-block;
        background: #1E293B;
        color: #E2E8F0;
        padding: 3px 10px;
        border-radius: 14px;
        font-size: 0.82rem;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid #334155;
    }

    /* Review flags */
    .review-flag-card {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
        color: #FDE68A;
        font-size: 0.9rem;
    }

    .verified-ok-card {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
        color: #A7F3D0;
        font-size: 0.9rem;
    }

    /* Status Pill */
    .status-pill-live {
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid #059669;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .status-pill-demo {
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid #D97706;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sarvam AI Processing Functions
# -----------------------------------------------------------------------------
def analyze_incident_with_sarvam(narrative_text: str, input_lang: str, api_key: str):
    """
    Calls Sarvam AI's sarvam-105b-conversations model to convert narrative text into
    structured incident JSON adhering to strict ethical & objective documentation rules.
    """
    from sarvamai import SarvamAI

    client = SarvamAI(api_subscription_key=api_key)

    system_instructions = (
        "You are CaseScribe, an objective, neutral legal-aid and incident documentation AI assistant.\n"
        "Your task is to analyze an incident narrative provided by a person and output a strictly structured JSON object.\n\n"
        "RULES FOR THE AI:\n"
        "1. Preserve the meaning and factual content of the original account faithfully.\n"
        "2. DO NOT INVENT names, dates, times, locations, evidence, motives, or events.\n"
        "3. Represent unknown or unstated information as null or an empty list.\n"
        "4. Distinguish what the narrator explicitly reports from information that is inferred, approximate, or unclear.\n"
        "5. Keep source excerpts linked to the original narrative where possible.\n"
        "6. Identify conflicting details as possible inconsistencies requiring human review, NOT proof of deception.\n"
        "7. DO NOT identify a suspect, determine guilt, assess credibility, or predict criminality.\n"
        "8. NEVER fabricate a timeline entry to fill missing information.\n"
        "9. Output MUST be ONLY valid JSON matching the exact schema below. No markdown backticks, no explanatory text."
    )

    schema_template = {
        "incident_summary": "Neutral factual summary of the account",
        "reported_events": [
            {
                "event_description": "What the person reports happened",
                "date": None,
                "time": None,
                "location": None,
                "people_mentioned": [],
                "source_excerpt": "Relevant original wording from narrative"
            }
        ],
        "people_mentioned": ["List of explicitly mentioned people/roles"],
        "locations_mentioned": ["List of explicitly mentioned locations"],
        "dates_and_times": ["List of explicitly mentioned dates or times"],
        "missing_information": ["List of critical gaps like exact times, addresses, or identifiers"],
        "clarification_questions": ["Neutral, non-leading questions to ask the narrator"],
        "potential_inconsistencies": ["List of potential internal ambiguities or conflicting statements"],
        "translated_summary": "Summary translated into English if input was Hindi/Marathi, or into Hindi/Marathi if input was English",
        "disclaimer": "This is an AI-organized account requiring human review."
    }

    user_prompt = f"""Analyze the incident narrative below and provide structured documentation in the exact JSON schema.

Input Language: {input_lang}

Schema to produce:
{json.dumps(schema_template, indent=2)}

Original Incident Narrative:
\"\"\"
{narrative_text}
\"\"\"
"""

    response = client.chat.completions(
        model="sarvam-105b-conversations",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,
    )

    raw_content = response.choices[0].message.content or ""
    
    # Clean and parse JSON
    clean_content = raw_content.strip()
    if clean_content.startswith("```"):
        # Strip code fences
        lines = clean_content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        clean_content = "\n".join(lines).strip()
    
    # Locate outer curly braces if text surrounds JSON
    first_brace = clean_content.find("{")
    last_brace = clean_content.rfind("}")
    if first_brace != -1 and last_brace != -1:
        clean_content = clean_content[first_brace:last_brace + 1]

    parsed_json = json.loads(clean_content)
    return parsed_json


def transcribe_audio_with_sarvam(audio_file, lang_code: str, api_key: str) -> str:
    """
    Transcribes uploaded audio using Sarvam AI Saaras Speech-to-Text API.
    """
    from sarvamai import SarvamAI

    client = SarvamAI(api_subscription_key=api_key)

    # Map general language names to Sarvam language codes
    code_map = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Marathi": "mr-IN",
        "Auto-Detect": "unknown"
    }
    sarvam_lang = code_map.get(lang_code, "unknown")

    file_payload = (audio_file.name, audio_file.getvalue(), audio_file.type or "audio/wav")

    response = client.speech_to_text.transcribe(
        file=file_payload,
        model="saaras:v3",
        language_code=sarvam_lang
    )
    return getattr(response, "transcript", "") or ""


# -----------------------------------------------------------------------------
# Sidebar: Configuration, Language, and Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ System Configuration")

    # API Key Input / Detection
    user_key = st.text_input(
        "Sarvam API Key",
        value=configured_key if configured_key else "",
        type="password",
        help="Reads automatically from .env or Streamlit secrets. You can also paste your key here."
    )

    active_key = user_key.strip() if user_key else configured_key

    # Live Mode vs Demo Mode Toggle
    st.markdown("---")
    st.markdown("### 🕹️ Execution Mode")
    demo_mode_manual = st.checkbox(
        "Force Demo Mode (Precomputed Output)",
        value=not bool(active_key),
        help="Use pre-calculated, verified responses without making external API calls. Ideal for offline demos."
    )

    is_demo_mode = demo_mode_manual or not bool(active_key)

    if not is_demo_mode:
        st.markdown('<span class="status-pill-live">🟢 LIVE SARVAM AI CONNECTED</span>', unsafe_allow_html=True)
        st.caption("Model: `sarvam-105b-conversations` + `saaras:v3`")
    else:
        st.markdown('<span class="status-pill-demo">🟡 DEMO MODE (Offline Precomputed)</span>', unsafe_allow_html=True)
        if not active_key:
            st.caption("ℹ️ No API key detected. Using verified demo output.")
        else:
            st.caption("ℹ️ Running in demo mode by manual toggle.")

    st.markdown("---")
    st.markdown("### 🌐 Language & Input Settings")
    input_language = st.selectbox(
        "Narrator's Spoken / Written Language",
        options=["English", "Marathi (मराठी)", "Hindi (हिन्दी)"],
        index=0,
        help="Select the language in which the user is providing their statement."
    )

    st.markdown("---")
    st.markdown("### 📌 Responsible AI Safeguards")
    st.caption(
        "• **Non-Inquisitorial**: Organizes statements without interrogating credibility.\n"
        "• **Zero Speculation**: Unwitnessed causes are preserved as unknown.\n"
        "• **Source-Linked**: Claims reference exact narrator excerpts.\n"
        "• **MIT-WPU Hackathon**: Built for rapid social-impact legal aid."
    )

# -----------------------------------------------------------------------------
# Main Header & Disclaimer
# -----------------------------------------------------------------------------
st.markdown("""
<div class="app-header-box">
    <div class="hackathon-badge">MIT-WPU Pune • AI Hackathon Edition</div>
    <h1 class="app-title">⚖️ CaseScribe</h1>
    <div class="app-tagline">Multilingual Crime Incident Documentation Assistant — From spoken account to structured incident report.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-banner">
    <strong>⚠️ Important Notice & Responsible Use:</strong> CaseScribe organizes preliminary accounts provided directly by the user. 
    It does <em>not</em> verify allegations, determine guilt, assess witness credibility, or substitute for professional legal counsel or official law enforcement investigations. 
    All generated information must be reviewed by qualified human personnel before legal or administrative use.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Step 1: Incident Input Section
# -----------------------------------------------------------------------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Step 1: Incident Narrative Input</div>', unsafe_allow_html=True)

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1.8, 1.8, 1.4])

with col_ctrl1:
    if st.button("📋 Load Pune College Scenario (English)", use_container_width=True):
        st.session_state["narrative_input"] = FICTIONAL_PUNE_SCENARIO_EN
        st.session_state["selected_lang"] = "English"

with col_ctrl2:
    if st.button("🚩 Load Pune College Scenario (मराठी)", use_container_width=True):
        st.session_state["narrative_input"] = FICTIONAL_PUNE_SCENARIO_MR
        st.session_state["selected_lang"] = "Marathi (मराठी)"

with col_ctrl3:
    if st.button("🗑️ Clear Form", use_container_width=True):
        st.session_state["narrative_input"] = ""
        st.session_state["processed_data"] = None

# Audio Upload Feature (Sarvam Saaras STT)
with st.expander("🎙️ Optional: Upload Spoken Audio Statement (Sarvam Saaras ASR)", expanded=False):
    st.write("Upload an audio recording of the incident statement (.wav, .mp3, .m4a, .ogg):")
    audio_file = st.file_uploader(
        "Select Audio Recording",
        type=["wav", "mp3", "m4a", "ogg", "aac", "webm", "flac"],
        label_visibility="collapsed"
    )

    if audio_file is not None:
        st.audio(audio_file)
        if st.button("⚡ Transcribe Audio with Sarvam Saaras", key="btn_transcribe"):
            if is_demo_mode or not active_key:
                st.info("🎙️ Demo Mode: Populated with sample transcription of the Pune college audio scenario.")
                st.session_state["narrative_input"] = FICTIONAL_PUNE_SCENARIO_EN
            else:
                with st.spinner("Transcribing audio using Sarvam Saaras API..."):
                    try:
                        transcript = transcribe_audio_with_sarvam(audio_file, input_language, active_key)
                        if transcript:
                            st.session_state["narrative_input"] = transcript
                            st.success("Audio successfully transcribed into the narrative box below!")
                        else:
                            st.warning("Transcription completed with empty output. Please verify audio clarity.")
                    except Exception as e:
                        st.error(f"Sarvam Audio Transcription error: {str(e)}")
                        st.info("Falling back to sample audio statement text for demonstration.")
                        st.session_state["narrative_input"] = FICTIONAL_PUNE_SCENARIO_EN

# Narrative text area
default_text = st.session_state.get("narrative_input", "")
narrative_text = st.text_area(
    "Describe the incident in detail (in English, Marathi, or Hindi):",
    value=default_text,
    height=160,
    placeholder="Example: Yesterday evening around 7:30 PM, I was near the main gate of a college in Pune. I saw a person wearing a dark jacket arguing with a delivery rider..."
)

generate_clicked = st.button("🚀 Generate Incident Report", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Step 2: Processing Logic
# -----------------------------------------------------------------------------
if generate_clicked:
    if not narrative_text.strip():
        st.error("Please provide an incident narrative or click 'Load Pune College Scenario' before generating.")
    else:
        with st.spinner("Processing account with Sarvam AI (Extracting events, timelines & checks)..."):
            if is_demo_mode:
                # Use robust pre-computed report
                st.session_state["processed_data"] = PRECOMPUTED_DEMO_REPORT
                st.session_state["used_mode"] = "demo"
                st.session_state["source_text"] = narrative_text
            else:
                try:
                    res_json = analyze_incident_with_sarvam(narrative_text, input_language, active_key)
                    st.session_state["processed_data"] = res_json
                    st.session_state["used_mode"] = "live"
                    st.session_state["source_text"] = narrative_text
                except Exception as ex:
                    st.error(f"Live Sarvam API call encountered an error: {str(ex)}")
                    st.info("Activating Demo Mode fallback to ensure uninterrupted presentation.")
                    st.session_state["processed_data"] = PRECOMPUTED_DEMO_REPORT
                    st.session_state["used_mode"] = "demo_fallback"
                    st.session_state["source_text"] = narrative_text

# -----------------------------------------------------------------------------
# Step 3: Results Dashboard
# -----------------------------------------------------------------------------
report_data = st.session_state.get("processed_data")

if report_data:
    st.markdown("---")
    
    # Mode indicator banner
    mode_used = st.session_state.get("used_mode", "demo")
    if mode_used == "live":
        st.success("✅ Report generated in real time using Sarvam AI `sarvam-105b-conversations`.")
    elif mode_used == "demo_fallback":
        st.warning("⚠️ Live API was temporarily unreachable; displaying verified fallback analysis.")
    else:
        st.info("ℹ️ Displaying verified demo analysis (Demo Mode).")

    # Section A: INCIDENT OVERVIEW
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Section A: Incident Overview</div>', unsafe_allow_html=True)

    summary_text = report_data.get("incident_summary", "No summary provided.")
    st.markdown(f"**Neutral Incident Summary:**")
    st.info(summary_text)

    # Translated Summary if present
    translated_sum = report_data.get("translated_summary")
    if translated_sum:
        with st.expander("🌐 Multilingual Cross-Translation (Summary)", expanded=False):
            st.markdown(f"*{translated_sum}*")

    # Metrics Row
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Reported Events", len(report_data.get("reported_events", [])))
    with m_col2:
        st.metric("Persons Mentioned", len(report_data.get("people_mentioned", [])))
    with m_col3:
        st.metric("Locations Mentioned", len(report_data.get("locations_mentioned", [])))
    with m_col4:
        st.metric("Clarifications Needed", len(report_data.get("clarification_questions", [])))

    st.markdown("<br>", unsafe_allow_html=True)

    # Entities Breakdown Chips
    c_p, c_l, c_d = st.columns(3)
    with c_p:
        st.markdown("**👥 People Mentioned:**")
        people = report_data.get("people_mentioned", [])
        if people:
            for p in people:
                st.markdown(f'<span class="tag-chip">{p}</span>', unsafe_allow_html=True)
        else:
            st.caption("None explicitly named")

    with c_l:
        st.markdown("**📍 Locations Mentioned:**")
        locations = report_data.get("locations_mentioned", [])
        if locations:
            for loc in locations:
                st.markdown(f'<span class="tag-chip">{loc}</span>', unsafe_allow_html=True)
        else:
            st.caption("None explicitly named")

    with c_d:
        st.markdown("**⏱️ Dates & Times Mentioned:**")
        dts = report_data.get("dates_and_times", [])
        if dts:
            for dt in dts:
                st.markdown(f'<span class="tag-chip">{dt}</span>', unsafe_allow_html=True)
        else:
            st.caption("None explicitly specified")

    st.markdown('</div>', unsafe_allow_html=True)

    # Section B: EVENT TIMELINE
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⏱️ Section B: Chronological Event Timeline</div>', unsafe_allow_html=True)
    st.caption("Note: Events with unknown timestamps are displayed in narrative sequence as reported. CaseScribe does not fabricate chronological order.")

    events = report_data.get("reported_events", [])

    if events:
        # Tabular View for investigators
        timeline_rows = []
        for idx, ev in enumerate(events, start=1):
            date_val = ev.get("date") or "Not specified"
            time_val = ev.get("time") or "Not specified"
            loc_val = ev.get("location") or "Not specified"
            desc_val = ev.get("event_description", "")
            excerpt = ev.get("source_excerpt", "")
            people_str = ", ".join(ev.get("people_mentioned", [])) if ev.get("people_mentioned") else "None"
            timeline_rows.append({
                "Seq #": idx,
                "Time / Date": f"{time_val} ({date_val})" if time_val != "Not specified" or date_val != "Not specified" else "Not specified",
                "Location": loc_val,
                "Reported Event": desc_val,
                "People Involved": people_str,
            })
        
        df_timeline = pd.DataFrame(timeline_rows)
        st.dataframe(df_timeline, use_container_width=True, hide_index=True)

        st.markdown("#### Sequential Event Cards & Source Provenance:")
        for idx, ev in enumerate(events, start=1):
            date_str = ev.get("date") or "Date not specified"
            time_str = ev.get("time") or "Time not specified"
            loc_str = ev.get("location") or "Location not specified"
            desc_str = ev.get("event_description", "No description")
            excerpt_str = ev.get("source_excerpt")

            st.markdown(f"""
            <div class="timeline-item">
                <span class="timeline-time-badge">Event #{idx} • {time_str} • {date_str}</span>
                <div style="font-weight: 500; color: #F1F5F9; font-size: 0.95rem;">{desc_str}</div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">📍 Reported Location: {loc_str}</div>
                {f'<div class="source-quote">“{excerpt_str}”</div>' if excerpt_str else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No distinct events extracted from statement.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Section C & D Columns
    col_c, col_d = st.columns(2)

    with col_c:
        # Section C: CLARIFICATION CHECKLIST
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔍 Section C: Clarification Checklist</div>', unsafe_allow_html=True)
        st.caption("Neutral follow-up inquiries to assist legal aid / caseworkers without suggesting answers.")

        missing_info = report_data.get("missing_information", [])
        if missing_info:
            st.markdown("**Identified Information Gaps:**")
            for item in missing_info:
                st.markdown(f"• {item}")
        else:
            st.caption("No critical missing information flagged.")

        questions = report_data.get("clarification_questions", [])
        if questions:
            st.markdown("<br>**Recommended Clarification Questions:**", unsafe_allow_html=True)
            for idx, q in enumerate(questions, start=1):
                st.checkbox(f"{q}", key=f"q_{idx}")
        else:
            st.caption("No clarification questions generated.")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        # Section D: REVIEW FLAGS
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🚩 Section D: Review Flags & Ambiguities</div>', unsafe_allow_html=True)
        st.caption("Potential inconsistencies or gaps requiring human review. (Does not prove deception or credibility).")

        inconsistencies = report_data.get("potential_inconsistencies", [])
        if inconsistencies:
            for item in inconsistencies:
                st.markdown(f"""
                <div class="review-flag-card">
                    <strong>⚠️ Requires Human Review:</strong><br>
                    {item}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="verified-ok-card">
                <strong>✅ No Direct Contradictions Detected:</strong><br>
                The narrative contains no direct internal conflicting statements. 
                <em>(Note: Absence of contradictions does not verify factual veracity; external evidence verification remains essential.)</em>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Step 4: Export Reports
    # -------------------------------------------------------------------------
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💾 Step 4: Export Incident Report</div>', unsafe_allow_html=True)

    # Plain text report formatter
    text_export_lines = [
        "=" * 72,
        "CASESCRIBE — STRUCTURED INCIDENT DOCUMENTATION REPORT",
        "Generated by: CaseScribe Multilingual AI Assistant (MIT-WPU AI Hackathon)",
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 72,
        "",
        "LEGAL & ETHICAL DISCLAIMER:",
        report_data.get("disclaimer", "This is an AI-organized account requiring human review."),
        "Notice: CaseScribe organizes preliminary accounts provided directly by the user.",
        "It does not verify allegations, determine guilt, assess witness credibility, or",
        "substitute for professional legal counsel or law enforcement investigation.",
        "",
        "-" * 72,
        "1. INCIDENT OVERVIEW",
        "-" * 72,
        f"Input Language: {input_language}",
        f"Summary: {summary_text}",
        f"Translated Summary: {translated_sum if translated_sum else 'N/A'}",
        "",
        f"People Mentioned: {', '.join(report_data.get('people_mentioned', [])) or 'None'}",
        f"Locations Mentioned: {', '.join(report_data.get('locations_mentioned', [])) or 'None'}",
        f"Dates & Times: {', '.join(report_data.get('dates_and_times', [])) or 'None'}",
        "",
        "-" * 72,
        "2. CHRONOLOGICAL EVENT TIMELINE",
        "-" * 72,
    ]

    for idx, ev in enumerate(events, start=1):
        text_export_lines.extend([
            f"Event #{idx}:",
            f"  Description : {ev.get('event_description')}",
            f"  Date        : {ev.get('date') or 'Not specified'}",
            f"  Time        : {ev.get('time') or 'Not specified'}",
            f"  Location    : {ev.get('location') or 'Not specified'}",
            f"  People      : {', '.join(ev.get('people_mentioned', [])) or 'None'}",
            f"  Source Text : \"{ev.get('source_excerpt', '')}\"",
            ""
        ])

    text_export_lines.extend([
        "-" * 72,
        "3. CLARIFICATION CHECKLIST & MISSING DETAILS",
        "-" * 72,
        "Missing Information Gaps:"
    ])
    for item in missing_info:
        text_export_lines.append(f"  • {item}")

    text_export_lines.append("\nRecommended Neutral Follow-up Inquiries:")
    for q in questions:
        text_export_lines.append(f"  [ ] {q}")

    text_export_lines.extend([
        "",
        "-" * 72,
        "4. REVIEW FLAGS & AMBIGUITIES",
        "-" * 72,
    ])
    if inconsistencies:
        for flag in inconsistencies:
            text_export_lines.append(f"  [!] Requires Human Review: {flag}")
    else:
        text_export_lines.append("  No direct internal contradictions detected in current statement.")

    text_export_lines.extend([
        "",
        "=" * 72,
        "ORIGINAL SUBMITTED NARRATIVE:",
        "=" * 72,
        st.session_state.get("source_text", narrative_text),
        "=" * 72,
    ])

    formatted_text_report = "\n".join(text_export_lines)
    formatted_json_report = json.dumps(report_data, indent=2, ensure_ascii=False)

    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        st.download_button(
            label="📄 Download Incident Report (.txt)",
            data=formatted_text_report,
            file_name=f"CaseScribe_Incident_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with exp_col2:
        st.download_button(
            label="📦 Download Structured Report (.json)",
            data=formatted_json_report,
            file_name=f"CaseScribe_Incident_Data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.8rem; margin-top: 40px; padding-top: 20px; border-top: 1px solid #1E293B;">
    CaseScribe • Multilingual Legal Aid & Incident Documentation System • Powered by Sarvam AI Models<br>
    Built for 45-minute AI Hackathon at MIT-WPU Pune • Designed for Social Impact
</div>
""", unsafe_allow_html=True)
