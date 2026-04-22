# SURAKSHA 🛡️
### Secure User Rural Authentication & Knowledge-driven Security Helper for Access

> **Problem Statement ID:** 25205 | **Organization:** Government of Odisha | **Department:** E & IT Department  
> **Theme:** Blockchain & Cybersecurity | **Category:** Software Prototype

---

A lightweight, AI-powered cybersecurity framework for securing digital banking transactions for rural users in Odisha. Built with Gemini AI agents, Machine Learning, Deep Learning, and NLP — optimized for low-end smartphones and limited internet connectivity.

---

## The Problem

Rural banking users in Odisha face a unique combination of challenges: low digital literacy, 2G/low connectivity, low-end smartphones (2GB RAM), and exposure to sophisticated fraud tactics. Existing banking security frameworks are designed for urban, high-bandwidth users and fail in this context — leaving millions vulnerable.

**SURAKSHA** addresses this with a ground-up, rural-first cybersecurity prototype targeting a **20% reduction in fraud incidents**.

---

## Key Features

### 1. 🔐 Adaptive Multi-Factor Authentication (AMFA)
Risk-aware authentication that adjusts challenge level based on real-time ML risk scoring.
- Low risk → PIN only
- Medium risk → SMS OTP
- High risk → Biometric + OTP
- Works **offline** with cached credentials for dead zones
- **Tech:** Logistic Regression, AES-256, SMS OTP

### 2. 🕵️ Real-Time Fraud Detection Engine
The core of SURAKSHA — a deep learning pipeline that monitors every transaction for anomalies.
- **LSTM** neural network detects suspicious transaction sequences
- **Random Forest** cross-validates every flag
- **Gemini Fraud Reasoning Agent** generates a human-readable verdict and recommended action
- **Tech:** TensorFlow Lite, Scikit-learn, Gemini API

### 3. 💬 Multilingual NLP Helpdesk Chatbot
An intelligent chatbot for rural users in **Odia, Hindi, and English**.
- Intent classification and Named Entity Recognition (NER)
- Sentiment analysis to detect distress signals (potential fraud coercion)
- Voice input via Web Speech API for low-literacy users
- **Tech:** BERT-lite, HuggingFace Transformers, Gemini LLM, Web Speech API

### 4. 📊 Transaction Monitoring Dashboard (Admin Panel)
Real-time dashboard for bank officers and administrators.
- Live fraud heatmap by district
- Transaction trend analytics
- AI-generated daily narrative reports (Gemini Report Agent)
- Role-based access control for officers
- **Tech:** React.js, WebSocket, Gemini API, Chart.js

### 5. 🛡️ Secure Transaction Gateway
Lightweight encryption layer optimized for low-spec Android devices.
- AES-256 encryption at rest, TLS 1.3 in transit
- ECDSA digital signatures for transaction integrity
- Certificate pinning against MITM attacks
- Offline transaction queue with replay-attack prevention via nonce tokens
- **Tech:** OpenSSL, Python Cryptography, ECDSA

### 6. 🧠 Behavioural Biometrics Profiler
Passive, continuous authentication — invisible to the user during normal use.
- Tracks typing rhythm, scroll speed, tap patterns, transaction timing
- Silently computes a trust score each session
- Triggers re-authentication only on significant deviation
- **Tech:** Isolation Forest, Autoencoder (Deep Learning)

### 7. 🔔 Smart Alert & User Education System
Intelligent, plain-language security alerts and personalised education.
- Native-language SMS and in-app push notifications on suspicious activity
- Gemini Education Agent delivers personalised security tips based on user risk profile
- NLP classifier auto-routes user-reported incidents to the right team
- **Tech:** Gemini API, NLP Text Classifier, SMS Gateway

### 8. 🔗 Audit Trail & Immutable Log (Blockchain-Lite)
A cryptographically chained, tamper-evident audit log satisfying the Blockchain & Cybersecurity theme.
- SHA-256 hash-chaining — every log entry links to the previous one
- Covers all auth events, transactions, fraud flags, and admin actions
- Natural language querying via Gemini Audit Query Agent ("show flagged transactions from Koraput last week")
- Exportable for regulatory compliance
- **Tech:** SHA-256 Hash Chaining, PostgreSQL, Gemini API

---

## Gemini AI Agents

SURAKSHA uses **6 specialized Gemini agents** coordinated by a master orchestrator:

| Agent | Role |
|---|---|
| **Risk Orchestrator Agent** | Master agent — coordinates all others, decides which agents to invoke per transaction event |
| **Fraud Reasoning Agent** | Reasons over ML flags, generates human-readable verdict and recommended action |
| **NLP Helpdesk Agent** | Drives the multilingual chatbot with intent detection and Odia/Hindi translation |
| **Report Digest Agent** | Generates daily narrative summaries of transaction and fraud data for bank officers |
| **Education Agent** | Produces personalised, simple-language security tips based on user risk profile |
| **Audit Query Agent** | Translates natural language admin queries into structured audit log searches |

---

## ML / DL / NLP Models

| Model | Type | Purpose | Module |
|---|---|---|---|
| LSTM Network | Deep Learning | Transaction sequence anomaly detection | Fraud Engine |
| Random Forest | ML | Cross-validation of fraud flags | Fraud Engine |
| Isolation Forest | ML | Behavioural anomaly detection | Biometric Profiler |
| Autoencoder | Deep Learning | User session behaviour reconstruction | Biometric Profiler |
| Logistic Regression | ML | Real-time risk scoring | Authentication (AMFA) |
| BERT-lite (Intent Classifier) | NLP | Chatbot intent detection | Helpdesk Bot |
| NER Model | NLP | Entity extraction from user messages | Helpdesk Bot |
| Sentiment Analyser | NLP | Detecting distress / coercion in chat | Helpdesk Bot |
| Text Classifier | NLP | Incident category routing | Alert System |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (PWA)                            │
│   React.js · Next.js · Offline-first · Web Speech API        │
│   Progressive Web App — works on 2G, low-end Android         │
└──────────────────────────┬──────────────────────────────────┘
                           │ TLS 1.3 + ECDSA
┌──────────────────────────▼──────────────────────────────────┐
│                   BACKEND API LAYER                          │
│   Python FastAPI · REST + WebSocket · JWT Auth               │
│   Celery Task Queue · Redis Cache · Rate Limiting            │
└────────────┬──────────────────────────┬─────────────────────┘
             │                          │
┌────────────▼──────────┐  ┌────────────▼────────────────────┐
│   AI / ML LAYER       │  │    DATA & SECURITY LAYER         │
│  Gemini API (Agents)  │  │  PostgreSQL (transactions)       │
│  TensorFlow Lite (DL) │  │  MongoDB (behaviour logs)        │
│  Scikit-learn (ML)    │  │  AES-256 + TLS 1.3               │
│  HuggingFace (NLP)    │  │  ECDSA · Cert Pinning            │
│  ONNX Model Serving   │  │  SHA-256 Hash-Chained Audit Log  │
└───────────────────────┘  └─────────────────────────────────┘
```

---

## Transaction Security Flow

```
[1] User opens PWA on low-end phone (works on 2G / offline queue)
        ↓
[2] AMFA: ML risk score computed → appropriate challenge level triggered
        ↓
[3] Transaction encrypted (AES-256) + signed (ECDSA) + nonce applied
        ↓
[4] LSTM + Random Forest fraud analysis on backend
        ↓
[5] If flagged → Gemini Risk Orchestrator → Fraud Reasoning Agent verdict
        ↓
[6] Action taken: Allow / Flag / Block
        ↓
[7] Alert sent in local language + Education tip + Audit log entry written
```

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React.js, Next.js, Tailwind CSS, Progressive Web App, Web Speech API |
| **Backend** | Python, FastAPI, Celery, Redis, WebSocket |
| **AI / Agents** | Google Gemini API, LangChain (agent orchestration) |
| **Deep Learning** | TensorFlow Lite, Keras (LSTM, Autoencoder) |
| **Machine Learning** | Scikit-learn (Random Forest, Isolation Forest, Logistic Regression) |
| **NLP** | HuggingFace Transformers (BERT-lite), spaCy (NER), NLTK |
| **Security / Crypto** | OpenSSL, Python Cryptography lib, ECDSA, AES-256, TLS 1.3 |
| **Database** | PostgreSQL, MongoDB |
| **Model Serving** | ONNX Runtime |
| **Notifications** | Firebase Cloud Messaging, SMS Gateway API |
| **DevOps** | Docker, GitHub Actions |

---

## Project Structure

```text
suraksha/
├── frontend/                  # React PWA
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── pages/             # App pages
│   │   ├── hooks/             # Custom React hooks
│   │   └── service-worker.js  # Offline support
│   └── public/
│
├── backend/                   # FastAPI backend
│   ├── api/
│   │   ├── auth/              # AMFA endpoints
│   │   ├── transactions/      # Transaction processing
│   │   ├── fraud/             # Fraud detection endpoints
│   │   └── admin/             # Admin dashboard API
│   ├── agents/                # Gemini AI agents
│   │   ├── orchestrator.py
│   │   ├── fraud_agent.py
│   │   ├── helpdesk_agent.py
│   │   ├── report_agent.py
│   │   ├── education_agent.py
│   │   └── audit_agent.py
│   ├── ml/                    # ML & DL models
│   │   ├── fraud_detection/   # LSTM + Random Forest
│   │   ├── biometrics/        # Isolation Forest + Autoencoder
│   │   └── risk_scoring/      # AMFA risk model
│   ├── nlp/                   # NLP pipeline
│   │   ├── intent_classifier.py
│   │   ├── ner_model.py
│   │   └── sentiment_analyser.py
│   ├── security/              # Crypto utilities
│   │   ├── encryption.py      # AES-256
│   │   ├── signatures.py      # ECDSA
│   │   └── audit_log.py       # Hash-chain logger
│   └── models/                # DB models
│
├── ml_training/               # Model training notebooks
│   ├── lstm_fraud_detection.ipynb
│   ├── behavioural_profiler.ipynb
│   └── nlp_pipeline.ipynb
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Google Gemini API key
- PostgreSQL 14+
- MongoDB 6+

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/suraksha.git
cd suraksha

# Set up environment variables
cp .env.example .env
# Add your GEMINI_API_KEY and DB credentials to .env

# Start all services with Docker
docker-compose up --build

# Or run manually:

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/suraksha
MONGODB_URI=mongodb://localhost:27017/suraksha
REDIS_URL=redis://localhost:6379
JWT_SECRET=your_jwt_secret
SMS_GATEWAY_API_KEY=your_sms_gateway_key
ENCRYPTION_KEY=your_aes_256_key
```

---

## Development Roadmap

| Phase | Duration | Deliverable |
|---|---|---|
| Phase 1 — Foundation | Weeks 1–3 | System design, DB schema, basic auth, encrypted API, PWA skeleton |
| Phase 2 — ML Models | Weeks 4–6 | LSTM + Random Forest training, behavioural profiler, AMFA risk scorer |
| Phase 3 — Gemini Agents | Weeks 7–9 | All 6 agents, chatbot NLP pipeline, Odia/Hindi language support |
| Phase 4 — Security Layer | Weeks 10–11 | AES/TLS/ECDSA integration, hash-chain audit log, offline queue |
| Phase 5 — Admin Dashboard | Weeks 12–14 | Bank officer panel, fraud heatmaps, alert management, report digests |
| Phase 6 — Testing & Demo | Weeks 15–16 | End-to-end testing, low-end device simulation, prototype demo |

---

## Expected Outcomes

- **20% reduction** in fraud incidents (measurable via before/after simulation on test dataset)
- Functional prototype supporting transactions on **2G connectivity**
- App footprint **under 50MB** for low-end smartphone compatibility
- **Multilingual support** — Odia, Hindi, English
- Fully auditable, tamper-evident transaction history
- Real-time fraud response with **sub-3-second alert delivery**

---

## Team

> Add your team member names, roles, and institute here.

| Name | Role |
|---|---|
| — | Full Stack Developer |
| — | ML / DL Engineer |
| — | NLP & AI Agent Developer |
| — | Security & Cryptography |
| — | UI/UX & Frontend |

---

## License

This project is developed as part of the Smart India Hackathon (SIH) 2025 for Problem Statement ID 25205, Government of Odisha, E & IT Department.

---

<div align="center">
  <strong>SURAKSHA</strong> — Protecting rural India's digital banking, one transaction at a time.
</div>
