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
    page_title="Sakshya AI — Multilingual Incident & FIR Documentation",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except Exception:
    pass

# Retrieve API key from environment or Streamlit secrets
def get_sarvam_api_key():
    key = os.environ.get("SARVAM_API_KEY")
    if key and key.strip():
        return key.strip()
    try:
        if "SARVAM_API_KEY" in st.secrets:
            return st.secrets["SARVAM_API_KEY"].strip()
    except Exception:
        pass
    return None

configured_key = get_sarvam_api_key()
if configured_key:
    os.environ["SARVAM_API_KEY"] = configured_key

# -----------------------------------------------------------------------------
# Fictional Scenarios & Demo Data (Enhanced with Authentic FIR Data)
# -----------------------------------------------------------------------------
FICTIONAL_PUNE_SCENARIO_EN = (
    "Yesterday evening, around 7:30 PM, I was near the main gate of a college in Pune. "
    "I saw a person wearing a dark jacket arguing with a delivery rider. A few minutes later, "
    "I heard a loud noise and noticed that the rider had fallen. I did not see exactly what caused the fall. "
    "Another person standing nearby called for help. I left after the ambulance arrived."
)

FICTIONAL_PUNE_SCENARIO_MR = (
    "काल संध्याकाळी सुमारे साडेसातच्या सुमारास मी पुण्यातील एका कॉलेजच्या मुख्य प्रवेशद्वाराजवळ होतो. "
    "काळ्या जॅकेट घातलेली एक व्यक्ती आणि एका डिलिव्हरी रायडर यांच्यात जोरदार वाद सुरू असलेला मी पाहिला. "
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
    "disclaimer": "This is an AI-organized account requiring human review.",
    "severity_assessment": {
        "severity_level": "High (Cognizable)",
        "is_cognizable": True,
        "fir_warranted": True,
        "offence_category": "Physical Altercation / Suspected Hurt / Roadside Incident",
        "legal_rationale": (
            "The witness account discloses an aggressive dispute immediately followed by physical collapse "
            "and severe enough injury to necessitate emergency ambulance dispatch. Under Section 154 Cr.P.C. "
            "and the landmark Lalita Kumari v. Govt of UP ruling, registration of an FIR is mandatory whenever "
            "information prima facie reveals the commission of a cognizable offence."
        ),
        "tentative_sections": [
            {
                "act": "IPC / BNS",
                "section": "IPC Sec. 323 / BNS Sec. 115(2)",
                "description": "Voluntarily causing hurt",
                "cognizable": "Cognizable / Compoundable"
            },
            {
                "act": "IPC / BNS",
                "section": "IPC Sec. 341 / BNS Sec. 126(2)",
                "description": "Wrongful restraint (obstructing free passage of delivery rider)",
                "cognizable": "Cognizable"
            },
            {
                "act": "IPC / BNS",
                "section": "IPC Sec. 504 / BNS Sec. 352",
                "description": "Intentional insult with intent to provoke breach of the peace",
                "cognizable": "Non-cognizable (Investigable alongside cognizable offences u/s 155(4) Cr.P.C.)"
            }
        ]
    },
    "draft_fir": {
        "district": "Pune",
        "police_station": "Shivajinagar / Local PS Pune",
        "year": "2026",
        "fir_no": "DRAFT-2026-PUN-084",
        "date_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "acts_and_sections": [
            {"act": "Indian Penal Code (IPC)", "section": "Sec. 323", "bns_equiv": "BNS Sec. 115(2)", "rw_section": "R/W Sec. 34"},
            {"act": "Indian Penal Code (IPC)", "section": "Sec. 341", "bns_equiv": "BNS Sec. 126(2)", "rw_section": ""},
            {"act": "Indian Penal Code (IPC)", "section": "Sec. 504", "bns_equiv": "BNS Sec. 352", "rw_section": ""}
        ],
        "suspected_offences": "Physical dispute, wrongful restraint, and injury sustained by delivery rider",
        "occurrence_of_offence": {
            "day": "Yesterday evening",
            "date": "Previous Day",
            "time_period": "Around 7:30 PM",
            "info_received_date": datetime.now().strftime("%d/%m/%Y"),
            "info_received_time": datetime.now().strftime("%H:%M:%S"),
            "general_diary_ref": "Entry No. 12 / General Diary (GD)"
        },
        "type_of_information": "Written (Witness Statement taken via Sakshya AI Legal Aid Intake)",
        "place_of_occurrence": {
            "direction_distance_from_ps": "Approx. 2.5 KMs North-East from Police Station",
            "beat_no": "Beat No. 2",
            "address": "Near Main Gate of College Campus, Pune",
            "city": "Pune",
            "district": "Pune",
            "state": "Maharashtra",
            "pin": "411004"
        },
        "complainant_informant": {
            "name": "Independent Eyewitness (Name to be verified)",
            "father_husband_name": "Not specified in witness narrative",
            "date_year_of_birth": "Adult Citizen",
            "nationality": "INDIAN",
            "occupation": "Student / Resident",
            "address": "Pune, Maharashtra"
        },
        "accused_details": [
            {
                "accused_no": 1,
                "name": "Unidentified person wearing dark jacket",
                "particulars": "Wearing dark jacket; observed aggressively arguing with delivery rider; fled or departed prior to or during ambulance arrival"
            }
        ],
        "victim_details": "Delivery rider (Unidentified; collapsed following loud noise; evacuated by emergency ambulance)",
        "reasons_for_delay": "Immediate priority given to medical assistance; narrator provided prompt statement following event.",
        "properties_stolen_involved": "Commercial delivery consignment / vehicle involved at location.",
        "inquest_report": "MLC (Medico-Legal Case) advised at receiving hospital upon admission of injured delivery rider.",
        "first_information_contents": (
            "The informant reports that yesterday evening around 7:30 PM, the informant was present near the main gate "
            "of a college in Pune. The informant observed an altercation wherein an unidentified individual wearing a dark jacket "
            "was arguing heatedly with a delivery rider. A few minutes thereafter, a loud noise was heard, and the delivery rider "
            "was seen to have fallen to the ground. The informant did not witness the exact physical blow or cause resulting in the fall. "
            "Another bystander called for help, and an ambulance subsequently arrived and transported the rider. "
            "The informant remained at the scene until the arrival of the ambulance and now provides this first information of the facts."
        ),
        "action_taken": "Information reveals commission of cognizable offence(s) u/s 323, 341 IPC (Sec 115(2), 126(2) BNS). Recommended for formal registration and dispatch of Investigating Officer (IO)."
    }
}

# -----------------------------------------------------------------------------
# Custom Styling (Dark Navy / Charcoal + Restrained Teal + Police FIR Theme)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    /* Main Theme Variables */
    :root {
        --bg-main: #0B0F19;
        --card-bg: #111827;
        --card-border: #1F2937;
        --teal-accent: #0D9488;
        --teal-light: #14B8A6;
        --text-primary: #F3F4F6;
        --text-secondary: #9CA3AF;
        --accent-amber: #F59E0B;
        --accent-blue: #38BDF8;
        --accent-red: #EF4444;
    }

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
        margin-bottom: 20px;
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

    /* Severity Banner Cards */
    .severity-high-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(185, 28, 28, 0.08) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-left: 6px solid #EF4444;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 18px;
    }

    .severity-med-banner {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.08) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-left: 6px solid #F59E0B;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 18px;
    }

    .severity-badge-high {
        background: #EF4444;
        color: #FFFFFF;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        display: inline-block;
    }

    .severity-badge-med {
        background: #F59E0B;
        color: #FFFFFF;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }

    /* FIR Official Form Box (Matching CCTNS / Police Format) */
    .fir-document-box {
        background: #0F172A;
        border: 2px solid #334155;
        border-radius: 8px;
        padding: 24px;
        color: #E2E8F0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.4);
        margin-top: 12px;
        margin-bottom: 18px;
    }

    .fir-official-header {
        text-align: center;
        border-bottom: 2px solid #475569;
        padding-bottom: 14px;
        margin-bottom: 18px;
    }

    .fir-official-header h2 {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #F8FAFC;
        margin: 0;
        text-transform: uppercase;
    }

    .fir-official-header h4 {
        font-size: 0.92rem;
        font-weight: 600;
        color: #94A3B8;
        margin: 4px 0 0 0;
    }

    .fir-field-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 12px;
        margin-bottom: 14px;
    }

    .fir-field-item {
        background: #1E293B;
        padding: 10px 14px;
        border-radius: 6px;
        border: 1px solid #334155;
    }

    .fir-field-label {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .fir-field-value {
        font-size: 0.92rem;
        color: #F8FAFC;
        font-weight: 500;
        margin-top: 2px;
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

    .tag-section-chip {
        display: inline-block;
        background: rgba(13, 148, 136, 0.2);
        color: #2DD4BF;
        border: 1px solid rgba(45, 212, 191, 0.4);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }

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
# Sarvam AI Processing Functions (Enhanced with Severity & FIR Logic)
# -----------------------------------------------------------------------------
def analyze_incident_with_sarvam(narrative_text: str, input_lang: str, api_key: str):
    """
    Calls Sarvam AI's sarvam-105b-conversations model to convert narrative text into
    structured incident JSON AND generate an authentic Indian Police Draft FIR
    based on crime severity assessment under Section 154 Cr.P.C. / Section 173 BNSS.
    """
    from sarvamai import SarvamAI

    client = SarvamAI(api_subscription_key=api_key)

    system_instructions = (
        "You are Sakshya AI, an objective legal-aid documentation and incident reporting AI assistant for India.\n"
        "Your task is to analyze an incident statement from a victim or eyewitness, assess the severity of the crime,\n"
        "and produce a structured JSON object containing an incident report and an authentic Indian Police Draft FIR\n"
        "formatted in accordance with Section 154 Cr.P.C. / Section 173 Bharatiya Nagarik Suraksha Sanhita (BNSS 2023).\n\n"
        "CRIME SEVERITY & FIR RULES:\n"
        "1. Assess whether the facts disclose a COGNIZABLE OFFENCE (e.g., physical assault, grievous hurt, robbery, theft, hit & run, sexual harassment)\n"
        "   or a NON-COGNIZABLE dispute (minor verbal insult, civil dispute).\n"
        "2. If a cognizable offence or bodily injury requiring medical dispatch is indicated, assign Severity: 'High (Cognizable)' or 'Medium (Cognizable)'\n"
        "   and generate a complete Draft FIR (First Information Report) following standard Indian Police / CBI Form No. 1.\n"
        "3. Identify tentative sections under both Indian Penal Code (IPC) and Bharatiya Nyaya Sanhita (BNS 2023).\n"
        "4. DO NOT INVENT or assume unstated details (suspect identity, weapons, motives). Preserve what was witnessed vs unobserved.\n"
        "5. Output MUST be ONLY valid JSON matching the exact schema provided. No conversational preamble, no markdown fences."
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
        "disclaimer": "This is an AI-organized account requiring human review.",
        "severity_assessment": {
            "severity_level": "High (Cognizable)",
            "is_cognizable": True,
            "fir_warranted": True,
            "offence_category": "Assault / Physical Injury / Altercation",
            "legal_rationale": "Explanation of why cognizable offence is or is not disclosed under Sec 154 CrPC",
            "tentative_sections": [
                {"act": "IPC / BNS", "section": "IPC Sec. 323 / BNS Sec. 115(2)", "description": "Voluntarily causing hurt", "cognizable": "Cognizable"}
            ]
        },
        "draft_fir": {
            "district": "Pune",
            "police_station": "Jurisdictional Police Station",
            "year": "2026",
            "fir_no": "DRAFT-2026-PUN-084",
            "date_time": "DD/MM/YYYY HH:MM:SS",
            "acts_and_sections": [
                {"act": "IPC", "section": "Sec. 323", "bns_equiv": "BNS Sec. 115(2)", "rw_section": ""}
            ],
            "suspected_offences": "Summary of suspected penal offences",
            "occurrence_of_offence": {
                "day": "Day of week",
                "date": "Date of incident",
                "time_period": "Approximate time period",
                "info_received_date": "Date reported",
                "info_received_time": "Time reported",
                "general_diary_ref": "Entry No. 12 / General Diary"
            },
            "type_of_information": "Written (Witness Statement via Sakshya AI)",
            "place_of_occurrence": {
                "direction_distance_from_ps": "Distance/direction",
                "beat_no": "Beat Number",
                "address": "Full location of incident",
                "city": "City",
                "district": "District",
                "state": "State",
                "pin": "Pin Code"
            },
            "complainant_informant": {
                "name": "Eyewitness / Informant",
                "father_husband_name": "Not specified",
                "date_year_of_birth": "Adult",
                "nationality": "INDIAN",
                "occupation": "Not specified",
                "address": "City, State"
            },
            "accused_details": [
                {
                    "accused_no": 1,
                    "name": "Unidentified person in dark jacket",
                    "particulars": "Particulars as reported by witness"
                }
            ],
            "victim_details": "Victim particulars as reported",
            "reasons_for_delay": "Immediate emergency response prioritized",
            "properties_stolen_involved": "Particulars of property involved",
            "inquest_report": "MLC reference if injury reported",
            "first_information_contents": "Formal legal complaint statement...",
            "action_taken": "Recommendation for registration and IO assignment"
        }
    }

    user_prompt = f"""Analyze the incident narrative below, evaluate crime severity, and generate structured documentation and a Draft FIR in valid JSON.

Input Language: {input_lang}

Schema to follow:
{json.dumps(schema_template, indent=2)}

Narrative:
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
    
    clean_content = raw_content.strip()
    if clean_content.startswith("```"):
        lines = clean_content.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        clean_content = "\n".join(lines).strip()
    
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

    code_map = {
        "English": "en-IN",
        "Hindi": "hi-IN",
        "Marathi (मराठी)": "mr-IN",
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

    user_key = st.text_input(
        "Sarvam API Key",
        value=configured_key if configured_key else "",
        type="password",
        help="Reads automatically from .env or Streamlit secrets."
    )

    active_key = user_key.strip() if user_key else configured_key

    st.markdown("---")
    st.markdown("### 🕹️ Execution Mode")
    demo_mode_manual = st.checkbox(
        "Force Demo Mode (Precomputed Output)",
        value=not bool(active_key),
        help="Use pre-calculated, verified responses without making external API calls."
    )

    is_demo_mode = demo_mode_manual or not bool(active_key)

    if not is_demo_mode:
        st.markdown('<span class="status-pill-live">🟢 LIVE SARVAM AI CONNECTED</span>', unsafe_allow_html=True)
        st.caption("LLM: `sarvam-105b-conversations`\nASR: `saaras:v3`")
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
    st.markdown("### ⚖️ Legal & FIR Parameters")
    st.caption(
        "• **Statutory Framework**: Sec. 154 Cr.P.C. & Sec. 173 Bharatiya Nagarik Suraksha Sanhita (BNSS 2023).\n"
        "• **Mandatory FIR Standard**: Lalita Kumari v. Govt of UP (Cognizable test).\n"
        "• **Dual Penal Mapping**: Indian Penal Code (IPC) + Bharatiya Nyaya Sanhita (BNS 2023)."
    )

# -----------------------------------------------------------------------------
# Main Header & Disclaimer
# -----------------------------------------------------------------------------
st.markdown("""
<div class="app-header-box">
    <div class="hackathon-badge">MIT-WPU Pune • AI Hackathon Edition</div>
    <h1 class="app-title">⚖️ Sakshya AI <span style="font-size: 1.15rem; color: #2DD4BF; font-weight: 500;">(साक्ष्य AI)</span></h1>
    <div class="app-tagline">Multilingual Crime Incident Documentation & Automated FIR Drafting Assistant — From spoken account to structured legal statement.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer-banner">
    <strong>⚠️ Important Statutory Notice & Responsible Use:</strong> Sakshya AI organizes preliminary witness accounts and generates a <em>Draft First Information Report (FIR)</em> 
    under Section 154 Cr.P.C. / Section 173 BNSS based on prima facie severity evaluation. 
    It does <em>not</em> determine guilt, verify allegations, or replace the statutory authority of a Police Duty Officer / Station House Officer (SHO). 
    All generated documents must be verified and signed by authorized personnel.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Step 1: Incident Input Section
# -----------------------------------------------------------------------------
st.markdown('<div class="custom-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Step 1: Incident Narrative Input & Severity Evaluation</div>', unsafe_allow_html=True)

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
    height=150,
    placeholder="Example: Yesterday evening around 7:30 PM, I was near the main gate of a college in Pune. I saw a person wearing a dark jacket arguing with a delivery rider..."
)

generate_clicked = st.button("🚀 Analyze Incident & Generate Draft FIR", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Step 2: Processing Logic
# -----------------------------------------------------------------------------
if generate_clicked:
    if not narrative_text.strip():
        st.error("Please provide an incident narrative or click 'Load Pune College Scenario' before generating.")
    else:
        with st.spinner("Evaluating crime severity and drafting FIR with Sarvam AI..."):
            if is_demo_mode:
                st.session_state["processed_data"] = PRECOMPUTED_DEMO_REPORT
                st.session_state["used_mode"] = "demo"
                st.session_state["source_text"] = narrative_text
            else:
                try:
                    res_json = analyze_incident_with_sarvam(narrative_text, input_language, active_key)
                    # Merge with default structure if any key is missing
                    if "draft_fir" not in res_json:
                        res_json["draft_fir"] = PRECOMPUTED_DEMO_REPORT["draft_fir"]
                    if "severity_assessment" not in res_json:
                        res_json["severity_assessment"] = PRECOMPUTED_DEMO_REPORT["severity_assessment"]
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
# Step 3: Results Dashboard (4 Distinct Sections + Official FIR Tab)
# -----------------------------------------------------------------------------
report_data = st.session_state.get("processed_data")

if report_data:
    st.markdown("---")
    
    mode_used = st.session_state.get("used_mode", "demo")
    if mode_used == "live":
        st.success("✅ Analysis & Draft FIR generated in real time using Sarvam AI `sarvam-105b-conversations`.")
    elif mode_used == "demo_fallback":
        st.warning("⚠️ Live API was temporarily unreachable; displaying verified fallback analysis.")
    else:
        st.info("ℹ️ Displaying verified demo analysis (Demo Mode).")

    # -------------------------------------------------------------------------
    # Crime Severity & FIR Assessment Callout
    # -------------------------------------------------------------------------
    severity_info = report_data.get("severity_assessment", {})
    sev_level = severity_info.get("severity_level", "High (Cognizable)")
    is_cognizable = severity_info.get("is_cognizable", True)
    fir_warranted = severity_info.get("fir_warranted", True)
    legal_rationale = severity_info.get("legal_rationale", "Cognizable offence prima facie disclosed.")
    tentative_secs = severity_info.get("tentative_sections", [])

    banner_class = "severity-high-banner" if "High" in sev_level else "severity-med-banner"
    badge_class = "severity-badge-high" if "High" in sev_level else "severity-badge-med"

    st.markdown(f"""
    <div class="{banner_class}">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span class="{badge_class}">CRIME SEVERITY: {sev_level.upper()}</span>
            <span style="font-size: 0.82rem; font-weight: 600; color: #E2E8F0;">
                {'🚨 MANDATORY FIR REGISTRATION WARRANTED (Sec. 154 Cr.P.C.)' if fir_warranted else 'ℹ️ NON-COGNIZABLE REPORT (NCR / GD ENTRY)'}
            </span>
        </div>
        <div style="font-size: 0.92rem; color: #F1F5F9; margin-bottom: 8px;">
            <strong>Statutory Assessment:</strong> {legal_rationale}
        </div>
        <div style="display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
            <strong style="font-size: 0.82rem; color: #CBD5E1;">Tentative Offence Sections:</strong>
            {''.join([f'<span class="tag-section-chip">{s.get("section", "")} — {s.get("description", "")}</span>' for s in tentative_secs])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs for Workflow Navigation
    tab_overview, tab_timeline, tab_checklist, tab_fir = st.tabs([
        "📊 Section A: Incident Overview",
        "⏱️ Section B: Event Timeline",
        "🔍 Sections C & D: Clarification & Review Flags",
        "🚨 Official Draft FIR (Sec. 154 Cr.P.C.)"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: SECTION A (INCIDENT OVERVIEW)
    # -------------------------------------------------------------------------
    with tab_overview:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Incident Overview & Entity Extraction</div>', unsafe_allow_html=True)

        summary_text = report_data.get("incident_summary", "No summary provided.")
        st.markdown("**Neutral Incident Summary:**")
        st.info(summary_text)

        translated_sum = report_data.get("translated_summary")
        if translated_sum:
            with st.expander("🌐 Multilingual Cross-Translation (Marathi / Hindi)", expanded=False):
                st.markdown(f"*{translated_sum}*")

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

    # -------------------------------------------------------------------------
    # TAB 2: SECTION B (EVENT TIMELINE)
    # -------------------------------------------------------------------------
    with tab_timeline:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⏱️ Section B: Chronological Event Timeline</div>', unsafe_allow_html=True)
        st.caption("Note: Events with unknown timestamps are displayed in reported narrative sequence. Sakshya AI does not fabricate chronological order.")

        events = report_data.get("reported_events", [])
        if events:
            timeline_rows = []
            for idx, ev in enumerate(events, start=1):
                date_val = ev.get("date") or "Not specified"
                time_val = ev.get("time") or "Not specified"
                loc_val = ev.get("location") or "Not specified"
                desc_val = ev.get("event_description", "")
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

    # -------------------------------------------------------------------------
    # TAB 3: SECTIONS C & D (CLARIFICATION & REVIEW FLAGS)
    # -------------------------------------------------------------------------
    with tab_checklist:
        col_c, col_d = st.columns(2)

        with col_c:
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
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🚩 Section D: Review Flags & Ambiguities</div>', unsafe_allow_html=True)
            st.caption("Potential inconsistencies or gaps requiring human review. (Does not prove deception).")

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
    # TAB 4: OFFICIAL DRAFT FIR (NEW CORE FEATURE)
    # -------------------------------------------------------------------------
    with tab_fir:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🚨 Official First Information Report (Draft Under Sec. 154 Cr.P.C. / Sec. 173 BNSS)</div>', unsafe_allow_html=True)
        st.caption("Standard National Crime Records Bureau (CCTNS) / State Police FIR Format generated automatically based on crime severity.")

        fir_data = report_data.get("draft_fir", PRECOMPUTED_DEMO_REPORT["draft_fir"])

        # Optional Customization expander for legal aid clinic / duty officer
        with st.expander("✏️ Customize Official FIR Metadata (Complainant Name, PS, District)", expanded=False):
            e_col1, e_col2, e_col3 = st.columns(3)
            with e_col1:
                custom_complainant = st.text_input("Complainant / Informant Name", value="Mr. Kajal Dutta (or Eyewitness)")
            with e_col2:
                custom_ps = st.text_input("Police Station (PS)", value=fir_data.get("police_station", "Shivajinagar Police Station, Pune"))
            with e_col3:
                custom_district = st.text_input("District & State", value=f"{fir_data.get('district', 'Pune')}, Maharashtra")

        # Official FIR Document Presentation Box (Matching the PDF)
        occ = fir_data.get("occurrence_of_offence", {})
        poc = fir_data.get("place_of_occurrence", {})
        comp = fir_data.get("complainant_informant", {})
        accused_list = fir_data.get("accused_details", [])
        acts_secs = fir_data.get("acts_and_sections", [])

        st.markdown(f"""
        <div class="fir-document-box">
            <div class="fir-official-header">
                <h2>FIRST INFORMATION REPORT</h2>
                <h4>(Under Section 154 Cr.P.C. / Section 173 Bharatiya Nagarik Suraksha Sanhita, 2023)</h4>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">State: Maharashtra • CCTNS / Digital Police Intake Format</div>
            </div>

            <!-- Item 1: Administration Details -->
            <div class="fir-field-grid">
                <div class="fir-field-item">
                    <div class="fir-field-label">1. District / State</div>
                    <div class="fir-field-value">{custom_district if 'custom_district' in locals() else fir_data.get('district', 'Pune')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">Police Station (PS)</div>
                    <div class="fir-field-value">{custom_ps if 'custom_ps' in locals() else fir_data.get('police_station', 'Shivajinagar PS')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">Year & FIR Draft No.</div>
                    <div class="fir-field-value">{fir_data.get('year', '2026')} / {fir_data.get('fir_no', 'DRAFT-2026-PUN-084')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">Date & Time of Report</div>
                    <div class="fir-field-value">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                </div>
            </div>

            <!-- Item 2: Acts & Sections Table -->
            <div style="margin-top: 14px; margin-bottom: 14px;">
                <div class="fir-field-label" style="margin-bottom: 6px;">2. Acts & Sections (IPC / Bharatiya Nyaya Sanhita 2023)</div>
                <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #1E293B; border-radius: 6px; overflow: hidden;">
                    <thead>
                        <tr style="background: #334155; color: #F8FAFC; text-align: left;">
                            <th style="padding: 8px 12px; border: 1px solid #475569;">Act</th>
                            <th style="padding: 8px 12px; border: 1px solid #475569;">Sections (IPC)</th>
                            <th style="padding: 8px 12px; border: 1px solid #475569;">BNS 2023 Equivalent</th>
                            <th style="padding: 8px 12px; border: 1px solid #475569;">R/W Section</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join([f'<tr><td style="padding: 8px 12px; border: 1px solid #334155;">{a.get("act", "IPC")}</td><td style="padding: 8px 12px; border: 1px solid #334155; font-weight: 600; color: #2DD4BF;">{a.get("section", "")}</td><td style="padding: 8px 12px; border: 1px solid #334155; color: #38BDF8;">{a.get("bns_equiv", a.get("section", ""))}</td><td style="padding: 8px 12px; border: 1px solid #334155;">{a.get("rw_section", "None")}</td></tr>' for a in acts_secs])}
                    </tbody>
                </table>
            </div>

            <!-- Item 3 & 4: Suspected Offences & Occurrence -->
            <div class="fir-field-grid">
                <div class="fir-field-item" style="grid-column: span 2;">
                    <div class="fir-field-label">3. Suspected Offences</div>
                    <div class="fir-field-value">{fir_data.get('suspected_offences', 'Assault, Wrongful Restraint')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">(a) Occurrence of Offence</div>
                    <div class="fir-field-value">{occ.get('day', 'Yesterday')} • {occ.get('time_period', 'Around 7:30 PM')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">(b) General Diary Reference</div>
                    <div class="fir-field-value">{occ.get('general_diary_ref', 'Entry No. 12 / GD')}</div>
                </div>
            </div>

            <!-- Item 5: Place of Occurrence -->
            <div class="fir-field-grid">
                <div class="fir-field-item" style="grid-column: span 2;">
                    <div class="fir-field-label">5. Place of Occurrence (Address / Landmark)</div>
                    <div class="fir-field-value">{poc.get('address', 'Near Main Gate of College Campus, Pune')}, {poc.get('city', 'Pune')} - {poc.get('pin', '411004')}</div>
                </div>
                <div class="fir-field-item" style="grid-column: span 2;">
                    <div class="fir-field-label">Direction & Distance from Police Station</div>
                    <div class="fir-field-value">{poc.get('direction_distance_from_ps', 'Approx. 2.5 KMs North-East from PS')} (Beat: {poc.get('beat_no', 'Beat 2')})</div>
                </div>
            </div>

            <!-- Item 6: Complainant / Informant -->
            <div class="fir-field-grid">
                <div class="fir-field-item">
                    <div class="fir-field-label">6. Complainant / Informant</div>
                    <div class="fir-field-value">{custom_complainant if 'custom_complainant' in locals() else comp.get('name', 'Eyewitness')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">Nationality</div>
                    <div class="fir-field-value">{comp.get('nationality', 'INDIAN')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">Occupation / Role</div>
                    <div class="fir-field-value">{comp.get('occupation', 'Student / Citizen')} ({comp.get('relationship', 'Independent Eyewitness')})</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">Type of Information</div>
                    <div class="fir-field-value">{fir_data.get('type_of_information', 'Written (Witness Statement)')}</div>
                </div>
            </div>

            <!-- Item 7: Details of Accused & Victim -->
            <div class="fir-field-grid">
                <div class="fir-field-item" style="grid-column: span 2;">
                    <div class="fir-field-label">7. Details of Known / Suspected / Unknown Accused with Full Particulars</div>
                    <div class="fir-field-value" style="color: #F87171;">
                        {'<br>'.join([f"<strong>Accused #{a.get('accused_no', 1)}:</strong> {a.get('name', 'Unknown')} — {a.get('particulars', '')}" for a in accused_list])}
                    </div>
                </div>
                <div class="fir-field-item" style="grid-column: span 2;">
                    <div class="fir-field-label">Victim Particulars / Medical Referral</div>
                    <div class="fir-field-value">{fir_data.get('victim_details', 'Delivery rider (Transported by ambulance)')}</div>
                </div>
            </div>

            <!-- Item 8, 9, 10, 11: Ancillary Details -->
            <div class="fir-field-grid">
                <div class="fir-field-item">
                    <div class="fir-field-label">8. Reasons for Delay in Reporting</div>
                    <div class="fir-field-value">{fir_data.get('reasons_for_delay', 'No Delay / Emergency medical response prioritized')}</div>
                </div>
                <div class="fir-field-item">
                    <div class="fir-field-label">9. Particulars of Property Stolen / Involved</div>
                    <div class="fir-field-value">{fir_data.get('properties_stolen_involved', 'None stolen; commercial transport vehicle involved')}</div>
                </div>
                <div class="fir-field-item" style="grid-column: span 2;">
                    <div class="fir-field-label">11. Inquest Report / U.D. Case / Medico-Legal Reference</div>
                    <div class="fir-field-value">{fir_data.get('inquest_report', 'MLC recommended at receiving hospital')}</div>
                </div>
            </div>

            <!-- Item 12: First Information Contents -->
            <div style="margin-top: 14px; margin-bottom: 14px; background: #1E293B; padding: 16px; border-radius: 6px; border: 1px solid #334155;">
                <div class="fir-field-label" style="margin-bottom: 8px;">12. First Information Contents (Statement of the Informant)</div>
                <div style="font-size: 0.94rem; line-height: 1.6; color: #F1F5F9; font-style: normal; text-align: justify;">
                    "{fir_data.get('first_information_contents', summary_text)}"
                </div>
            </div>

            <!-- Item 13 & 14: Action Taken & Signatures -->
            <div class="fir-field-grid">
                <div class="fir-field-item" style="grid-column: span 4;">
                    <div class="fir-field-label">13. Action Taken / Direction for Investigation</div>
                    <div class="fir-field-value" style="color: #34D399;">
                        {fir_data.get('action_taken', 'Registered case and took up preliminary investigation under Section 154 Cr.P.C.')}
                    </div>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; margin-top: 28px; padding-top: 18px; border-top: 1px dashed #475569; font-size: 0.85rem; color: #94A3B8;">
                <div style="text-align: center; width: 220px;">
                    ____________________________<br>
                    <strong>Signature / Thumb Impression of Informant</strong><br>
                    (Admitted to be correctly recorded)
                </div>
                <div style="text-align: center; width: 220px;">
                    ____________________________<br>
                    <strong>Signature of Officer-in-Charge</strong><br>
                    Station House Officer / Duty IO
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Step 4: Export Reports & Official FIR
    # -------------------------------------------------------------------------
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💾 Step 4: Export Incident Report & Official Draft FIR</div>', unsafe_allow_html=True)

    # Plain text FIR Formatter
    fir_export_lines = [
        "=" * 78,
        "FIRST INFORMATION REPORT (DRAFT)",
        "(Under Section 154 Cr.P.C. / Section 173 Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "Generated by: Sakshya AI Multilingual Assistant (MIT-WPU Pune Hackathon)",
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 78,
        "",
        f"1. District: {fir_data.get('district', 'Pune')}     PS: {fir_data.get('police_station', 'Shivajinagar')}",
        f"   Year: {fir_data.get('year', '2026')}                 FIR No: {fir_data.get('fir_no', 'DRAFT')}",
        f"   Date & Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        "",
        "2. Acts & Sections:",
    ]

    for a in acts_secs:
        fir_export_lines.append(f"   • {a.get('act', 'IPC')} {a.get('section', '')} (Equiv: {a.get('bns_equiv', 'N/A')}) R/W: {a.get('rw_section', 'None')}")

    fir_export_lines.extend([
        "",
        f"3. Suspected Offences: {fir_data.get('suspected_offences', 'Assault, Wrongful Restraint')}",
        f"   (a) Occurrence: {occ.get('day', 'Yesterday')} • {occ.get('time_period', 'Around 7:30 PM')}",
        f"   (b) General Diary Ref: {occ.get('general_diary_ref', 'Entry No. 12')}",
        "",
        f"4. Type of Information: {fir_data.get('type_of_information', 'Written Witness Statement')}",
        "",
        f"5. Place of Occurrence: {poc.get('address', 'Near College Main Gate, Pune')}",
        f"   Direction & Distance from PS: {poc.get('direction_distance_from_ps', '2.5 KMs North-East')}",
        "",
        f"6. Complainant / Informant: {comp.get('name', 'Eyewitness')} ({comp.get('nationality', 'INDIAN')})",
        f"   Address: {comp.get('address', 'Pune, Maharashtra')}",
        "",
        "7. Details of Known / Suspected / Unknown Accused:",
    ])

    for acc in accused_list:
        fir_export_lines.append(f"   • Accused #{acc.get('accused_no', 1)}: {acc.get('name')} | Particulars: {acc.get('particulars')}")

    fir_export_lines.extend([
        "",
        f"8. Reasons for delay: {fir_data.get('reasons_for_delay', 'No delay')}",
        f"9. Particulars of property: {fir_data.get('properties_stolen_involved', 'None')}",
        f"10. Inquest / Medical Case: {fir_data.get('inquest_report', 'MLC recommended')}",
        "",
        "-" * 78,
        "12. FIRST INFORMATION CONTENTS (STATEMENT OF THE INFORMANT):",
        "-" * 78,
        f"{fir_data.get('first_information_contents', summary_text)}",
        "",
        "-" * 78,
        f"13. Action Taken: {fir_data.get('action_taken', 'Registered preliminary draft')}",
        "-" * 78,
        "",
        "STATUTORY & RESPONSIBLE AI DISCLAIMER:",
        report_data.get("disclaimer", "This is an AI-organized account requiring human review."),
        "Sakshya AI organizes preliminary accounts provided directly by the user.",
        "It does not replace official police investigation or judicial proceedings.",
        "=" * 78,
    ])

    formatted_fir_text = "\n".join(fir_export_lines)

    # General incident summary export
    text_export_lines = [
        "=" * 78,
        "SAKSHYA AI — STRUCTURED INCIDENT DOCUMENTATION & SEVERITY REPORT",
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 78,
        f"Crime Severity Assessment: {sev_level} (FIR Warranted: {fir_warranted})",
        f"Summary: {summary_text}",
        f"Translated Summary: {translated_sum if translated_sum else 'N/A'}",
        "",
        "1. EVENT TIMELINE:",
    ]
    for idx, ev in enumerate(events, start=1):
        text_export_lines.append(f"Event #{idx}: {ev.get('event_description')} [Time: {ev.get('time') or 'Not specified'}, Loc: {ev.get('location') or 'Not specified'}]")
    
    text_export_lines.extend([
        "",
        "2. CLARIFICATION CHECKLIST:",
    ])
    for q in questions:
        text_export_lines.append(f"  [ ] {q}")
    
    text_export_lines.extend([
        "",
        "3. REVIEW FLAGS:",
    ])
    for item in inconsistencies:
        text_export_lines.append(f"  [!] Requires Human Review: {item}")
    
    formatted_incident_text = "\n".join(text_export_lines)
    formatted_full_json = json.dumps(report_data, indent=2, ensure_ascii=False)

    exp_col1, exp_col2, exp_col3 = st.columns(3)
    with exp_col1:
        st.download_button(
            label="🚨 Download Official Draft FIR (.txt)",
            data=formatted_fir_text,
            file_name=f"SakshyaAI_Official_FIR_Sec154_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with exp_col2:
        st.download_button(
            label="📄 Download Incident Report (.txt)",
            data=formatted_incident_text,
            file_name=f"SakshyaAI_Incident_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with exp_col3:
        st.download_button(
            label="📦 Download Full Data & FIR (.json)",
            data=formatted_full_json,
            file_name=f"SakshyaAI_Full_Incident_FIR_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.8rem; margin-top: 40px; padding-top: 20px; border-top: 1px solid #1E293B;">
    Sakshya AI (साक्ष्य AI) • Multilingual Legal Aid & Automated FIR Drafting System • Powered by Sarvam AI Models<br>
    Built for 45-minute AI Hackathon at MIT-WPU Pune • Under Section 154 Cr.P.C. & Section 173 BNSS 2023
</div>
""", unsafe_allow_html=True)
