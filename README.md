# ⚖️ CaseScribe — Multilingual Crime Incident Documentation Assistant

> **MIT-WPU Pune • 45-Minute AI Hackathon MVP**  
> *"From spoken account to structured incident report."*

CaseScribe is an objective, multilingual incident documentation assistant engineered for legal aid clinics, community support groups, and preliminary investigative teams. It empowers victims and witnesses who are more comfortable speaking Marathi, Hindi, or other Indian languages to provide preliminary statements and transforms raw, unstructured accounts into structured, chronological incident reports.

---

## 🎯 1. Product Vision & Problem Statement

* **The Problem:** Documenting incidents under distress is challenging. Citizens in India often articulate details more naturally in Marathi or Hindi than in formal legal English. Critical sequence data, timestamps, and witness positions are frequently lost or distorted during manual note-taking.
* **The Solution:** CaseScribe transcribes spoken or written statements, organizes information into structured chronological events, tracks source excerpts for provenance, highlights unstated details via neutral questions, and flags potential ambiguities for human review.
* **Responsible Boundary:** CaseScribe is a *documentation assistant*, **not** an automated police adjudication system. It does not assess credibility, determine guilt, or invent missing facts.

---

## 🚀 2. Core Features & Capabilities

1. **Multilingual Narrative Input:**
   - Supports native English, Marathi (मराठी), and Hindi (हिन्दी).
   - One-click loading of the fictional Pune college scenario.
2. **Sarvam AI Language Intelligence:**
   - Powered by `sarvam-105b-conversations` for structured entity and timeline extraction.
   - Powered by Sarvam `saaras:v3` for speech-to-text audio transcription.
   - Multilingual cross-summary generation.
3. **Four-Part Results Dashboard:**
   - **Section A (Incident Overview):** Neutral factual summary, entity tags (people, locations, dates/times).
   - **Section B (Chronological Timeline):** Structured tabular and card-based event progression, explicit marking of `"Not specified"` timestamps, and direct quote excerpts.
   - **Section C (Clarification Checklist):** Gap identification and neutral, non-leading follow-up questions.
   - **Section D (Review Flags):** Objective identification of conflicting details and ambiguities marked `"Requires human review"`.
4. **Dual Export Formats:**
   - Downloadable formatted `.txt` incident summary report.
   - Machine-readable `.json` payload for downstream legal-tech integrations.
5. **Zero-Failure Demo Mode:**
   - Seamless offline fallback with precomputed analysis of the Pune college scenario if an API key is absent or network is restricted.

---

## 🛡️ 3. Responsible AI Safeguards

CaseScribe displays a persistent disclaimer:
> *"CaseScribe organizes information provided by the user. It does not verify allegations, determine guilt, assess credibility, or replace professional legal advice. Review all generated information before use."*

* **No Speculation:** If the narrator reports not seeing what caused a fall, CaseScribe preserves that uncertainty and never infers a cause.
* **Zero Accusations:** Does not assign suspect status or legal fault.
* **Provenance Tracking:** Every timeline card references the original verbatim excerpt.

---

## 🛠️ 4. Tech Stack

* **Frontend:** Streamlit 1.x
* **AI & Language Processing:** Sarvam AI SDK (`sarvamai`)
  * `sarvam-105b-conversations` (Chat Completions & Schema Extraction)
  * `saaras:v3` (Speech-to-Text Transcription)
* **Data Processing:** Pandas, Datetime
* **Configuration:** `python-dotenv` / Streamlit secrets

---

## ⚡ 5. Quick Start Guide

### Prerequisites
- Python 3.10+
- Sarvam AI API Key (from [dashboard.sarvam.ai](https://dashboard.sarvam.ai))

### Installation
```bash
# Clone or navigate to the directory
cd C:\Users\haars\.gemini\antigravity\scratch\sarvam-project

# Install dependencies
pip install -r requirements.txt
```

### Configure Credentials
Copy `.env.example` to `.env` and set your API key:
```env
SARVAM_API_KEY=your_sarvam_api_key_here
```
*(The `.env` file is already added to `.gitignore` to prevent credential leaks.)*

### Launch the Application
```bash
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8501`.

---

## 🧪 6. Hackathon Live Demo Sequence

Follow these steps for the 45-minute hackathon evaluation:

1. **Load Fictional Scenario:** Click **"Load Pune College Scenario (English)"** (or Marathi) to populate the narrator's statement:
   > *"Yesterday evening, around 7:30 PM, I was near the main gate of a college in Pune. I saw a person wearing a dark jacket arguing with a delivery rider. A few minutes later, I heard a loud noise and noticed that the rider had fallen. I did not see exactly what caused the fall. Another person standing nearby called for help. I left after the ambulance arrived."*
2. **Generate Report:** Click **"🚀 Generate Incident Report"**.
3. **Inspect Overview:** Review the neutral summary and entity extraction chips.
4. **Examine Timeline:** Note that the argument, loud noise, fall, bystander call, and ambulance arrival are structured into chronological cards, with the fall's cause noted as unobserved.
5. **Review Clarification Checklist:** View neutral investigative questions (e.g. asking for specific calendar date, college name, noise origin).
6. **Inspect Review Flags:** Note the ambiguity flag advising against assuming causation between the dispute and the fall.
7. **Download Report:** Click **"Download Incident Report (.txt)"** or **"Download Structured Report (.json)"**.
8. **Demonstrate Responsible AI:** Highlight the persistent disclaimer and ethical safeguards.
