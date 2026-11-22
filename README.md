# 💙 Arogya Setu Senior+

An AI-powered elderly care and health monitoring web application with dedicated **Senior** and **Caregiver** portals. It combines voice-enabled AI companionship, real-time health risk assessment, medication adherence tracking, and automated caregiver email alerts.

Built with **Streamlit**, **FastAPI**, **OpenAI (`gpt-4o-mini`)**, and **Excel/Pandas** storage.

---

## ✨ Features

### 🔐 Role-Based Authentication (`ui/auth.py`)
- Separate **Senior** and **Caregiver** accounts stored in `data/users.xlsx`.
- Seniors link directly to a registered Caregiver during signup.

### 👴 Senior Dashboard (`ui/senior_dashboard.py`)
- **Voice & Text AI Companion:** Talk via microphone (`SpeechRecognition`, `en-IN`) or type messages to a supportive AI companion (`gpt-4o-mini`) that reads responses aloud (`pyttsx3`) and uses the senior's latest vitals for context.
- **Health Vitals & Risk Scoring:** Log **Blood Pressure**, **Sugar Level**, and **Heart Rate** to the FastAPI backend (`POST /submit-health`) for instant risk classification:
  - `High Risk`: BP > 160, Sugar > 250, or HR > 120 *(triggers spoken warning + caregiver email alert)*
  - `Warning`: BP > 140, Sugar > 180, or HR > 100
  - `Normal`: Within safe thresholds
- **Health Overview & History:** View latest vitals as metric cards and browse the last 7 logged records.
- **Smart Medication Reminders:** Displays prescribed medicines with allowed time windows. Seniors can mark doses as **Taken**; missed doses automatically send a one-time email alert to the caregiver.

### 👨‍⚕️ Caregiver Dashboard (`ui/caregiver_dashboard.py`)
- **My Seniors:** View all seniors assigned to the caregiver.
- **Prescribe Medication:** Create medication reminders with custom start and end time windows.
- **Medication Adherence (%):** Visual bar chart tracking adherence rates per senior.
- **Health Trends:** Side-by-side **Matplotlib** line charts for Blood Pressure, Sugar Level, and Heart Rate across the last 7 records.

---

## 📂 Project Structure

```text
arogya-setu-senior-plus/
├── app.py                        # Streamlit entry point & sidebar navigation
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
├── backend/
│   ├── api.py                    # FastAPI server (/submit-health endpoint)
│   ├── email_alert.py            # Gmail SMTP alerts (high risk & missed meds)
│   ├── reminder_storage.py       # Excel CRUD for medication reminders
│   ├── risk_logic.py             # Health risk threshold helper
│   ├── storage.py                # Excel storage for per-senior health records
│   ├── user_storage.py           # Excel storage for user auth & caregiver mapping
│   └── utils/constants.py        # Vital sign threshold constants
├── companion/
│   ├── chatbot.py                # OpenAI GPT-4o-mini health-aware companion
│   ├── voice_companion.py        # End-to-end voice chat pipeline
│   ├── voice_input.py            # Speech-to-text with Bluetooth/Realtek mic selection
│   ├── voice_output.py           # Threaded offline text-to-speech (pyttsx3)
│   ├── check_mic.py              # Utility to list available microphones
│   ├── temp.py                   # Utility to list available TTS voices
│   └── test_voice.py             # Utility to test microphone recognition
├── ui/
│   ├── auth.py                   # Login & Signup UI
│   ├── senior_dashboard.py       # Senior portal UI
│   └── caregiver_dashboard.py    # Caregiver portal UI
└── data/                         # Auto-generated Excel files (users, reminders, health logs)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, Matplotlib |
| **Backend API** | FastAPI, Uvicorn |
| **AI & Voice** | OpenAI (`gpt-4o-mini`), SpeechRecognition, pyttsx3 |
| **Data Storage** | Excel (`.xlsx`) via Pandas & OpenPyXL |
| **Notifications** | Python `smtplib` (Gmail SMTP) |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```
> **Note:** For microphone voice input with `SpeechRecognition`, ensure `PyAudio` is installed (`pip install pyaudio`).

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```env
OPENAI_API_KEY=your_openai_api_key
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_RECEIVER=caregiver@gmail.com
```
*(Use a [Google App Password](https://myaccount.google.com/apppasswords) for `EMAIL_PASSWORD` rather than your regular Gmail password.)*

---

## 🖥️ Running the Application

Start both the **FastAPI backend** and the **Streamlit frontend** in separate terminals from the project root directory.

### 1. Start the FastAPI Backend
```bash
uvicorn backend.api:app --reload
```
- API root: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### 2. Start the Streamlit Frontend
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser. Register a **Caregiver** account first, then register a **Senior** account and link it to that caregiver.

---

## ⚠️ Disclaimer

This application is a prototype built for **educational and hackathon purposes** and is not a certified medical device. Always consult a qualified healthcare professional for medical advice or emergencies.
