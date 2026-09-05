# CyberShield VisionX — Complete Project Documentation

> **Platform:** AI-Powered Cybercrime Detection & Victim Assistance System  
> **Version:** 2.0 (Production-Ready Upgrade)  
> **Stack:** Python · PyTorch · FastAPI · React · Ollama (LLaMA 3)  

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Directory Structure](#3-directory-structure)
4. [Block 1 — Transaction Risk Engine](#4-block-1--transaction-risk-engine)
5. [Block 2 — Phishing & Malware Scanner](#5-block-2--phishing--malware-scanner)
6. [Block 3 — Victim Assistant Chatbot](#6-block-3--victim-assistant-chatbot)
7. [API Gateway](#7-api-gateway)
8. [Frontend — CyberShield Console](#8-frontend--cybershield-console)
9. [ML Models & AI Tools](#9-ml-models--ai-tools)
10. [Datasets](#10-datasets)
11. [End-to-End Workflow](#11-end-to-end-workflow)
12. [Tech Stack Reference](#12-tech-stack-reference)
13. [Running the System](#13-running-the-system)

---

## 1. Project Overview

CyberShield VisionX is a full-stack cybercrime detection and victim support platform designed for law enforcement, cybersecurity teams, and the general public. It combines traditional rule-based heuristics with deep learning ML models and a local LLM (Large Language Model) to deliver real-time, explainable threat intelligence.

### Core Capabilities

| Capability | Description |
|---|---|
| **Transaction Risk Scoring** | Detects fraudulent financial transactions using a PyTorch Autoencoder + rule engine |
| **URL Phishing Detection** | Scans URLs using ML feature extraction and heuristic rules |
| **SMS/Message Scam Detection** | Classifies suspicious messages using NLP + Random Forest |
| **APK Malware Analysis** | Scans Android APK files against known hash signatures |
| **LLM Victim Assistant** | Empathetic chatbot powered by LLaMA 3 via Ollama for cybercrime victims |
| **Law Enforcement Console** | Real-time dashboard showing live anomaly-scored transaction data |
| **Explainable AI (XAI)** | Every threat verdict includes a human-readable reason powered by LLaMA 3 |

---

## 2. System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                     CyberShield Console (React)                    │
│          localhost:8080  ·  Vite + TypeScript + TailwindCSS        │
│                                                                    │
│  /                    Home Page                                    │
│  /scam-detection       → ScamDetection.tsx  (Block 2)              │
│  /victim-assistance    → VictimAssistance.tsx (Block 3)            │
│  /law-enforcement-console → LawEnforcementConsole.tsx (Block 1)   │
│  /awareness            → Awareness.tsx                             │
│  /contact              → Contact.tsx                               │
└────────────────────────┬───────────────────────────────────────────┘
                         │  HTTP REST (fetch, JSON)
                         ▼
┌────────────────────────────────────────────────────────────────────┐
│               API Gateway  (FastAPI · Python)                      │
│                      localhost:8000                                │
│                                                                    │
│  GET  /api/transactions  →  Block 1 hybrid_risk.py                │
│  POST /api/scan          →  Block 2 url / text / apk scanners     │
│  POST /api/chat          →  Block 3 chatbot_manager.py            │
└──────┬──────────────────┬──────────────────┬───────────────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌───────────────────┐
│   Block 1    │  │   Block 2    │  │     Block 3        │
│  Transaction │  │  Phishing /  │  │  Victim Assistant  │
│  Risk Engine │  │  Malware     │  │  LLM Chatbot       │
│  PyTorch AE  │  │  Scanners    │  │  Ollama LLaMA 3    │
└──────────────┘  └──────────────┘  └───────────────────┘
                                              │
                                              ▼
                                   ┌──────────────────┐
                                   │  Ollama Server   │
                                   │  localhost:11434  │
                                   │  llama3:latest   │
                                   └──────────────────┘
```

---

## 3. Directory Structure

```
CSH__VisionX/
│
├── api_gateway.py                  ← Central FastAPI server (all blocks united here)
│
├── block1_transaction_engine/
│   ├── hybrid_risk.py              ← Main orchestrator: rule + autoencoder hybrid
│   ├── rules.py                    ← Heuristic rule engine (4 fraud rules)
│   ├── train_model.py              ← Training pipeline entry point
│   ├── processor.py                ← Batch processing entry point
│   ├── sample_transactions.csv     ← Demo transaction data
│   ├── paysim dataset.csv          ← Large-scale PaySim training data (~493 MB)
│   ├── ae_model_v2.pth             ← Trained Autoencoder weights (PyTorch)
│   ├── ae_scaler_v2.pkl            ← Fitted StandardScaler (joblib)
│   └── ml_model/
│       ├── autoencoder.py          ← PyTorch Autoencoder model definition
│       ├── feature_engineering.py  ← Feature extraction pipeline
│       └── train_anomaly.py        ← Standalone training script
│
├── block2_phishing_scanner/
│   ├── scanner.py                  ← URL scan CLI entry
│   ├── sms_scanner.py              ← SMS scan CLI entry
│   ├── sms_scam_model.pkl          ← Trained Random Forest for SMS (joblib)
│   ├── url_phishing_model.pkl      ← Trained Random Forest for URLs (joblib)
│   ├── url_scanner/
│   │   ├── hybrid_url_risk.py      ← URL hybrid scorer (ML + rules)
│   │   ├── url_features.py         ← URL feature extractor
│   │   ├── url_rules.py            ← URL heuristic rules
│   │   └── url_model.py            ← URL ML model loader
│   ├── text_scanner/
│   │   ├── hybrid_text_risk.py     ← SMS hybrid scorer (ML + rules)
│   │   ├── message_model.py        ← NLP feature extractor + model trainer
│   │   └── nlp_rules.py            ← Text heuristic rules
│   └── malware_scanner/
│       ├── hybrid_apk_risk.py      ← APK hybrid risk scorer
│       ├── hash_checker.py         ← MD5 hash matching against known malware
│       └── apk_rules.py            ← APK static analysis rules
│
├── block3_victim_assistant/
│   ├── chatbot_manager.py          ← Main chatbot orchestrator
│   ├── llm_engine.py               ← Ollama REST API caller (LLaMA 3)
│   ├── intent_detector.py          ← Keyword-based victim context detector
│   ├── language_style.py           ← Language detector (English/Tamil/Tanglish)
│   ├── reassurance.py              ← Empathetic opening phrase generator
│   ├── guidance_rules.py           ← Context-aware safety advice
│   ├── context_memory.py           ← Per-session risk flag tracker
│   ├── chatbot_cli.py              ← CLI chatbot runner
│   ├── cyber_guard.py              ← Safety boundary enforcer
│   └── system_prompt.txt           ← LLM system persona and rules
│
└── cybershield-console/            ← React frontend (Vite + TypeScript)
    ├── src/
    │   ├── App.tsx                 ← Router setup
    │   ├── pages/
    │   │   ├── Home.tsx
    │   │   ├── ScamDetection.tsx   ← Calls /api/scan
    │   │   ├── VictimAssistance.tsx← Calls /api/chat
    │   │   ├── LawEnforcementConsole.tsx ← Calls /api/transactions
    │   │   ├── Awareness.tsx
    │   │   └── Contact.tsx
    │   └── components/
    │       ├── Navbar.tsx
    │       ├── RiskBadge.tsx       ← LOW / MEDIUM / HIGH badge component
    │       ├── Layout.tsx
    │       └── ui/                 ← Shadcn/Radix UI component library
    └── package.json
```

---

## 4. Block 1 — Transaction Risk Engine

### Purpose
Detects fraudulent financial transactions using a hybrid of heuristic business rules and a deep-learning Autoencoder anomaly detector.

### File: `rules.py` — Heuristic Rule Engine

The `RuleEngine` class applies 4 fraud detection rules per account:

| Rule | Trigger | Score |
|---|---|---|
| `sudden_spike` | More than 5 transactions from one account | +30 |
| `quick_in_out` | Consecutive transactions less than 30 min apart | +10 each (max +25) |
| `many_recipients` | More than 3 unique receiver accounts | +20 |
| `multiple_devices` | More than 1 unique device ID used | +15 |

**Maximum Heuristic Score: 90**

### File: `ml_model/feature_engineering.py` — Feature Pipeline

Transforms raw transaction rows into one aggregated feature row per account:

| Feature | Description |
|---|---|
| `tx_count` | Total number of transactions |
| `total_amount` | Sum of all transaction amounts |
| `mean_amount` | Average transaction amount |
| `std_amount` | Standard deviation of amounts |
| `unique_receivers` | Number of distinct receivers |
| `unique_devices` | Number of distinct device IDs |
| `hours_active_span` | Time span between first and last transaction (hours) |
| `tx_per_hour` | Transaction frequency rate |
| `proportion_night_tx` | Fraction of transactions between 12 AM–5 AM |
| `velocity_score` | `tx_per_hour × log(1 + mean_amount)` — combined speed/amount signal |
| `median_inter_tx_seconds` | Median gap between consecutive transactions |

**PaySim Adapter:** Automatically renames PaySim columns (`nameOrig` → `sender_account`, `nameDest` → `receiver_account`, `step` → `timestamp`) if detected.

### File: `ml_model/autoencoder.py` — PyTorch Autoencoder

**Model Architecture:**

```
Input (N features)
    ↓
Linear(N → 32) + ReLU
    ↓
Linear(32 → 16) + ReLU
    ↓
Linear(16 → 8)          ← Latent Space (compressed representation)
    ↓
Linear(8 → 16) + ReLU
    ↓
Linear(16 → 32) + ReLU
    ↓
Linear(32 → N)          ← Reconstruction Output
```

**Training:** Trained as a self-supervised model. The loss is MSE between the input and its reconstruction. Normal transactions reconstruct well (low loss). Fraudulent transactions reconstruct poorly (high loss = high anomaly score).

**Optimizer:** Adam · **Loss:** MSELoss · **Epochs:** 15–50 (adaptive)

**Key Functions:**

| Function | Description |
|---|---|
| `train_autoencoder(X, epochs)` | Trains model, returns model + fitted StandardScaler |
| `predict_anomaly_scores(model, scaler, X)` | Returns per-row MSE reconstruction error |
| `get_feature_contributions(model, scaler, X, names)` | Returns top-2 anomalous features per row (XAI) |

### File: `hybrid_risk.py` — Hybrid Orchestrator

**Scoring Formula:**
```
hybrid_score = (0.6 × rule_score) + (0.4 × ml_score_normalized)
```

**Risk Level Thresholds:**

| Score | Risk Level |
|---|---|
| > 60 | 🔴 HIGH |
| 30–60 | 🟡 MEDIUM |
| < 30 | 🟢 LOW |

**Smart Model Loading:** If `ae_model_v2.pth` is missing or empty, the system automatically trains a new Autoencoder using PaySim data (sampled to 100,000 rows for CPU efficiency). Uses `tempfile` + `shutil` to avoid OneDrive/Windows file-locking.

---

## 5. Block 2 — Phishing & Malware Scanner

### 5a. URL Scanner

**File: `url_scanner/url_features.py`** — Extracts 10 numerical features from any URL:

| Feature | Description |
|---|---|
| `url_length` | Total character length |
| `has_ip` | 1 if URL contains raw IP address |
| `has_https` | 1 if HTTPS protocol |
| `num_dots` | Number of `.` characters |
| `num_hyphens` | Number of `-` characters |
| `num_slashes` | Number of `/` characters |
| `has_at` | 1 if `@` symbol present |
| `keyword_count` | Count of suspicious words (login, verify, bank, upi, etc.) |
| `domain_length` | Length of the domain name |
| `subdomain_length` | Length of subdomain |
| `is_valid_url` | 1 if passes validators.url() |

**File: `url_scanner/url_rules.py`** — Heuristic scoring:

| Rule | Score |
|---|---|
| Raw IP address in URL | +30 |
| No HTTPS | +20 |
| `@` symbol in URL | +15 |
| ≥ 4 dots | +15 |
| Length > 60 chars | +10 |
| ≥ 2 suspicious keywords | +25 |
| Invalid URL format | +20 |

**Hybrid Formula:** `0.6 × rule_score + 0.4 × ML_probability`

**Verdicts:** `PHISHING` (>70) · `SUSPICIOUS` (>40) · `SAFE`

### 5b. SMS / Message Scanner

**File: `text_scanner/message_model.py`** — Extracts 8 NLP features:

| Feature | Description |
|---|---|
| `text_length` | Character count of message |
| `word_count` | Word count |
| `digit_count` | Number of digits |
| `has_url` | 1 if `http` or `www` present |
| `has_otp_word` | 1 if word "otp" present |
| `keyword_count` | Count of scam keywords |
| `urgent_words` | 1 if urgent language detected |
| `has_bank_word` | 1 if bank/upi/account mentioned |

**ML Model:** Random Forest Classifier (300 trees, balanced class weights)

**Hybrid Formula:** `0.7 × rule_score + 0.3 × ML_probability`

**Verdicts:** `SCAM` (>70) · `SUSPICIOUS` (>40) · `SAFE`

### 5c. APK / Malware Scanner

**File: `malware_scanner/hash_checker.py`** — Computes MD5 hash of APK file and matches against a known malware signature database.

**File: `malware_scanner/apk_rules.py`** — Static analysis rules (dangerous permissions, suspicious package names, etc.)

**Verdicts:** `MALWARE` (score≥70 or hash match) · `SUSPICIOUS` (≥40) · `SAFE`

### 5d. LLM Explainability (NEW in v2)

When a URL or message is flagged as HIGH or MEDIUM risk, the API Gateway automatically sends a prompt to the local Ollama LLaMA 3 model to generate a 2-sentence human-readable explanation of why the content is dangerous. This explanation is displayed in the React frontend.

---

## 6. Block 3 — Victim Assistant Chatbot

### Purpose
An empathetic AI chatbot that helps cybercrime victims stay calm and take the right steps. Powered by a locally running LLaMA 3 model via Ollama with a carefully crafted system prompt.

### File: `system_prompt.txt` — LLM Persona
- Treats all users as victims first
- Never blames or threatens
- Calm first, then actionable guidance
- Never requests OTP/PIN/passwords
- Encourages reporting without fear

### File: `language_style.py` — Multilingual Detector
Automatically detects the user's language and adapts the AI's response accordingly:

| Detected Style | Trigger |
|---|---|
| `english` | Default |
| `tanglish` | Contains words like "bayama", "romba", "emaathitanga" |
| `tamil_spoken` | Contains Tamil Unicode script (U+0B80–U+0BFF) |
| `mixed` | Both Tamil script AND Tanglish words present |

### File: `intent_detector.py` — Victim Context Filter
Scans user input for cybersecurity-related keywords before passing to the LLM. If none are matched, the bot politely declines (boundary enforcement).

**Supported keyword categories:** scam, fraud, OTP, bank, phishing, malware, hacked, stolen, password, link, click, download, virus, SMS, email, account, police, arrest, and more.

### File: `llm_engine.py` — Ollama REST Integration
Sends prompts to Ollama's local REST API (`http://127.0.0.1:11434/api/generate`):

```python
payload = {
    "model": "llama3:latest",
    "prompt": f"{system_prompt}\nINSTRUCTION: {style}\nUSER: {input}\nASSISTANT:",
    "stream": False,
    "options": {"temperature": 0.4, "top_p": 0.9}
}
```

**Temperature 0.4** — Keeps responses factual and consistent while remaining empathetic.

### File: `chatbot_manager.py` — Orchestrator
Full response pipeline:
1. Check intent (is it cybersecurity-related?)
2. Detect language style
3. Generate empathetic opening (`reassurance.py`)
4. Call LLaMA 3 via `llm_engine.py`
5. Append safety footer (OTP warning, 1930 helpline, cybercrime.gov.in)

---

## 7. API Gateway

**File:** `api_gateway.py`  
**Framework:** FastAPI + Uvicorn  
**Port:** `8000`  
**CORS:** Open (allows all origins for local development)

### Endpoints

#### `GET /api/transactions`
- Reads 10 random rows from PaySim dataset (or `sample_transactions.csv`)
- Runs `calculate_hybrid_risk()` from Block 1
- Returns JSON array with: `accountId`, `riskScore`, `riskLevel`, `amount`, `destination`, `timestamp`, `anomaly_reason`

#### `POST /api/scan`
**Body:** `{ "type": "url" | "message" | "apk", "content": "..." }`
- Routes to the appropriate Block 2 scanner
- Normalizes verdict to: `high` / `medium` / `low`
- Calls Ollama LLaMA 3 to generate XAI explanation for HIGH/MEDIUM results
- Returns: `risk`, `explanation`, `recommendations[]`

#### `POST /api/chat`
**Body:** `{ "message": "..." }`
- Routes to Block 3 `get_response()`
- Returns: `{ "response": "..." }`

---

## 8. Frontend — CyberShield Console

**Framework:** React 18 + TypeScript + Vite  
**Styling:** TailwindCSS + Shadcn/Radix UI  
**State:** TanStack React Query  
**Routing:** React Router DOM v6  
**Port:** `8080`

### Pages

| Route | Component | Connected To |
|---|---|---|
| `/` | `Home.tsx` | Static landing page |
| `/scam-detection` | `ScamDetection.tsx` | `POST /api/scan` |
| `/victim-assistance` | `VictimAssistance.tsx` | `POST /api/chat` |
| `/law-enforcement-console` | `LawEnforcementConsole.tsx` | `GET /api/transactions` |
| `/awareness` | `Awareness.tsx` | Static content |
| `/contact` | `Contact.tsx` | Static form |

### Key UI Components

- **`RiskBadge.tsx`** — Renders color-coded LOW / MEDIUM / HIGH badges
- **`Navbar.tsx`** — Navigation with links to all pages
- **`ScamDetection.tsx`** — Tab switcher for URL vs SMS scan, displays risk + LLM explanation
- **`VictimAssistance.tsx`** — Full chat UI with async API calls to LLaMA 3 backend
- **`LawEnforcementConsole.tsx`** — Live transaction table with filters, risk scores, anomaly reasons

---

## 9. ML Models & AI Tools

| Model | Type | Used In | File |
|---|---|---|---|
| **TransactionAutoencoder** | PyTorch Neural Network (Encoder-Decoder) | Block 1 | `autoencoder.py` |
| **StandardScaler** | Feature normalization | Block 1 | `ae_scaler_v2.pkl` |
| **Random Forest Classifier** | Scikit-learn (300 trees) | Block 2 URL | `url_phishing_model.pkl` |
| **Random Forest Classifier** | Scikit-learn (300 trees) | Block 2 SMS | `sms_scam_model.pkl` |
| **LLaMA 3 (8B)** | Local LLM via Ollama | Block 3 + XAI | `ollama run llama3` |
| **MinMaxScaler** | Score normalization 0–100 | Block 1 | In-memory |

### Ollama Models Available

| Model | Size | Purpose |
|---|---|---|
| `llama3:latest` | 4.7 GB | Primary chatbot + XAI explanations |
| `OpenNix/wazuh-llama-3.1-8B-base` | 4.7 GB | Available, security-tuned variant |
| `qwen3.5:latest` | 6.6 GB | Available |

---

## 10. Datasets

| Dataset | Location | Size | Purpose |
|---|---|---|---|
| **PaySim** | `block1_transaction_engine/paysim dataset.csv` | ~493 MB | Large-scale synthetic financial fraud dataset for Autoencoder training |
| **sample_transactions.csv** | `block1_transaction_engine/` | ~318 B | Minimal fallback demo data |
| **sample_sms.csv** | `block2_phishing_scanner/` | ~493 B | SMS scam training data |
| **sample_urls.csv** | `block2_phishing_scanner/` | ~1.1 KB | URL phishing training data |

### PaySim Column Mapping (Auto-Adapter)

| PaySim Column | System Column |
|---|---|
| `nameOrig` | `sender_account` |
| `nameDest` | `receiver_account` |
| `step` | `timestamp` (hours from Jan 1 2025) |
| `amount` | `amount` |

---

## 11. End-to-End Workflow

### Transaction Risk Analysis

```
User opens Law Enforcement Console
    ↓
React fetches GET http://localhost:8000/api/transactions
    ↓
api_gateway.py reads PaySim CSV (10 random rows)
    ↓
calculate_hybrid_risk(df)
    ├── extract_features(df)       → 11 features per account
    ├── RuleEngine.score_account() → heuristic score (0–90)
    ├── load_or_train_model()      → loads ae_model_v2.pth
    ├── predict_anomaly_scores()   → MSE reconstruction error
    ├── get_feature_contributions()→ top-2 anomalous features (XAI)
    └── hybrid_score = 0.6×rule + 0.4×ml_normalized
    ↓
JSON response → React renders table with RiskBadge + anomaly_reason
```

### URL / SMS Phishing Detection

```
User pastes URL or message in Scam Detection page
    ↓
React POSTs to POST http://localhost:8000/api/scan
    ↓
api_gateway.py routes to analyze_url() or analyze_text()
    ├── extract features (10 URL features or 8 text features)
    ├── heuristic rule_score()
    ├── ML model.predict_proba() → fraud probability
    └── hybrid_score = weighted combination
    ↓
If HIGH or MEDIUM risk:
    LLaMA 3 generates 2-sentence explanation
    ↓
JSON: { risk, explanation, recommendations[] }
    ↓
React displays risk badge + LLM explanation card
```

### Victim Assistance Chatbot

```
User types message in Victim Assistance chat
    ↓
React POSTs to POST http://localhost:8000/api/chat
    ↓
chatbot_manager.get_response(message)
    ├── intent_detector.is_victim_context() → keyword check
    ├── language_style.response_style()     → English/Tamil/Tanglish
    ├── reassurance()                        → empathetic opener
    ├── llm_engine.ask_llm()
    │       └── POST http://127.0.0.1:11434/api/generate
    │               model: llama3:latest
    │               temperature: 0.4
    └── append safety footer (1930 helpline, cybercrime.gov.in)
    ↓
JSON: { response: "..." }
    ↓
React renders assistant message in chat bubble
```

---

## 12. Tech Stack Reference

### Backend

| Tool | Version | Role |
|---|---|---|
| Python | 3.12 | Core language |
| FastAPI | Latest | REST API gateway |
| Uvicorn | Latest | ASGI server |
| PyTorch | Latest | Autoencoder deep learning |
| Scikit-learn | Latest | Random Forest, scalers |
| Pandas | Latest | Data manipulation |
| NumPy | Latest | Numerical operations |
| SciPy | Latest | Rank normalization |
| Joblib | Latest | Model serialization |
| Requests | Latest | Ollama REST calls |
| tldextract | Latest | URL domain parsing |
| validators | Latest | URL format validation |
| Ollama | 0.21.2 | Local LLM runtime |
| LLaMA 3 | 8B | Language model |

### Frontend

| Tool | Version | Role |
|---|---|---|
| React | 18.3.1 | UI framework |
| TypeScript | 5.8 | Type safety |
| Vite | 5.4 | Build tool + dev server |
| TailwindCSS | 3.4 | Utility-first styling |
| Shadcn/UI | Latest | Component library |
| Radix UI | Latest | Accessible primitives |
| React Router | 6.30 | Client-side routing |
| TanStack Query | 5.83 | Async state management |
| Lucide React | 0.462 | Icon library |
| Recharts | 2.15 | Data visualization |

---

## 13. Running the System

### Prerequisites

```powershell
# Python dependencies
pip install fastapi uvicorn pydantic pandas numpy torch scikit-learn scipy joblib requests tldextract validators

# Frontend dependencies (inside cybershield-console/)
npm install

# Ollama must be installed and running
ollama run llama3
```

### Start Backend (Terminal 1)

```powershell
# From CSH__VisionX root
python api_gateway.py
# Server starts at http://localhost:8000
```

### Start Frontend (Terminal 2)

```powershell
# From CSH__VisionX/cybershield-console/
npm run dev
# UI available at http://localhost:8080
```

### API Documentation
FastAPI auto-generates interactive docs at: `http://localhost:8000/docs`

### Train Block 1 Model (optional, auto-trains on first run)

```powershell
cd block1_transaction_engine
python train_model.py
# Saves ae_model_v2.pth and ae_scaler_v2.pkl
```

---

*Documentation generated: April 2026 | CyberShield VisionX v2.0*
