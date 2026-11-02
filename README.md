# ⚖️ Sakshya AI (साक्ष्य AI) — Multilingual Crime Incident Documentation & Automated FIR Drafting Assistant

> **MIT-WPU Pune • 45-Minute AI Hackathon MVP**  
> *"From spoken account to structured legal evidence & Section 154 Cr.P.C. Draft FIR."*

**Sakshya AI (साक्ष्य AI)** is an objective, multilingual incident documentation and legal aid assistant engineered for legal aid clinics, police station digital intake kiosks, community support groups, and preliminary investigative teams. It empowers victims and witnesses who are more comfortable speaking Marathi, Hindi, or other Indian languages to provide preliminary statements and transforms raw, unstructured accounts into structured, chronological incident reports and **authentic Draft First Information Reports (FIRs)** based on crime severity assessment.

---

## 🎯 1. Product Vision & Problem Statement

* **The Problem:** Documenting incidents under distress is challenging. Citizens in India often articulate details more naturally in Marathi or Hindi than in formal legal English. Critical sequence data, timestamps, and witness positions are frequently lost or distorted. Furthermore, identifying whether an incident constitutes a **Cognizable Offence** requiring an immediate FIR under Section 154 Cr.P.C. / Section 173 BNSS often creates friction for victims at police duty desks.
* **The Solution:** Sakshya AI transcribes spoken or written statements, organizes information into structured chronological events, assesses crime severity, identifies tentative IPC and BNS 2023 sections, and generates an authentic **14-point Draft First Information Report (FIR)** matching the standard National Crime Records Bureau (CCTNS) police form.
* **Responsible Boundary:** Sakshya AI is a *documentation assistant*, **not** an autonomous law enforcement system. It organizes statements, highlights gaps, and generates drafts without determining guilt or assessing witness credibility.

---

## 🚨 2. Core Feature: Automated FIR Drafting & Crime Severity Assessment

Based on the witness's narrative, Sakshya AI performs automated statutory evaluation:

1. **Crime Severity Evaluation:**
   - **High Severity (Cognizable):** Physical violence, assault, grievous hurt, robbery, hit-and-run, sexual harassment. Triggers mandatory FIR recommendation as per *Lalita Kumari v. Govt of UP*.
   - **Medium Severity (Cognizable):** Theft, cheating, criminal intimidation, criminal breach of trust.
   - **Low Severity (Non-Cognizable):** Minor verbal spats or civil disputes (diverts to Non-Cognizable Report / General Diary entry).
2. **Dual Penal Code Mapping:**
   - Indian Penal Code (IPC) (e.g. IPC Sec. 323, 341, 504, 506).
   - New Bharatiya Nyaya Sanhita (BNS 2023) equivalents (e.g. BNS Sec. 115(2), 126(2), 352).
3. **Authentic 14-Point CCTNS Police FIR Form:**
   - Follows the official Indian Police / CBI First Information Report format (Under Section 154 Cr.P.C. / Section 173 BNSS).
   - District, Police Station, Year, and FIR Draft Number.
   - Formal Acts & Sections Grid with R/W Section details.
   - Occurrence of Offence & General Diary (GD) reference.
   - Place of Occurrence (Beat No., distance & direction from PS).
   - Complainant / Informant particulars (with interactive editor).
   - Accused particulars (distinguishing reported descriptions from unobserved details).
   - First Information Contents (formal, legally sound statement of facts).
   - Action Taken & Investigating Officer (IO) direction.

---

## 🚀 3. Additional Capabilities

1. **Multilingual Narrative Input:**
   - Supports native English, Marathi (मराठी), and Hindi (हिन्दी).
   - One-click loading of the fictional Pune college scenario.
2. **Sarvam AI Language Intelligence:**
   - Powered by `sarvam-105b-conversations` for structured entity, timeline, and FIR extraction.
   - Powered by Sarvam `saaras:v3` for speech-to-text audio transcription.
   - Multilingual cross-summary generation.
3. **Four-Part Results Dashboard:**
   - **Section A (Incident Overview):** Neutral factual summary, entity tags (people, locations, dates/times).
   - **Section B (Chronological Timeline):** Structured tabular and card-based event progression, explicit marking of `"Not specified"` timestamps, and direct quote excerpts.
   - **Section C (Clarification Checklist):** Gap identification and neutral, non-leading follow-up questions.
   - **Section D (Review Flags):** Objective identification of conflicting details and ambiguities marked `"Requires human review"`.
4. **Triple Export Formats:**
   - Downloadable formatted `.txt` official Draft FIR (CCTNS Form layout).
   - Downloadable formatted `.txt` incident summary report.
   - Machine-readable `.json` payload containing the entire incident data and FIR schema.
5. **Zero-Failure Demo Mode:**
   - Seamless offline fallback with precomputed analysis and FIR of the Pune college scenario.

---

## 🛡️ 4. Responsible AI Safeguards

Sakshya AI displays a persistent disclaimer:
> *"Sakshya AI organizes preliminary witness accounts and generates a Draft First Information Report (FIR) under Section 154 Cr.P.C. / Section 173 BNSS based on prima facie severity evaluation. It does not determine guilt, verify allegations, or replace the statutory authority of a Police Duty Officer / Station House Officer (SHO). All generated documents must be verified and signed by authorized personnel."*

* **No Speculation:** If the narrator reports not seeing what caused a fall, Sakshya AI preserves that uncertainty and never infers a cause.
* **Zero Accusations:** Does not assign suspect status or legal fault.
* **Provenance Tracking:** Every timeline card references the original verbatim excerpt.

---

## 🛠️ 5. Tech Stack

* **Frontend:** Streamlit 1.x
* **AI & Language Processing:** Sarvam AI SDK (`sarvamai`)
  * `sarvam-105b-conversations` (Chat Completions, Severity & FIR Schema Extraction)
  * `saaras:v3` (Speech-to-Text Transcription)
* **Data Processing:** Pandas, Datetime
* **Configuration:** `python-dotenv` / Streamlit secrets

---

## ⚡ 6. Quick Start Guide

### Prerequisites
- Python 3.10+
- Sarvam AI API Key (from [dashboard.sarvam.ai](https://dashboard.sarvam.ai))

### Installation & Launch
```bash
# Navigate to the project directory
cd C:\Users\haars\.gemini\antigravity\scratch\sarvam-project

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The application will launch in your browser at `http://localhost:8502`.
