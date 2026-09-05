# CyberShield VisionX

AI-Powered Cybercrime Detection & Victim Assistance System.

CyberShield is a full-stack platform that helps **citizens, organizations, and law enforcement** detect scams, analyze financial fraud, and support cybercrime victims — powered by rule-based heuristics, deep-learning models, and a local LLaMA 3 LLM (via Ollama).

| Layer | Tech | Port |
|---|---|---|
| Frontend (CyberShield Console) | React 18 · TypeScript · Vite · Tailwind · shadcn/ui | `:8080` |
| Backend (API Gateway) | Python · FastAPI · Uvicorn | `:8000` |
| ML / Heuristics | PyTorch Autoencoder · Random Forest · rule engines | — |
| LLM | LLaMA 3 via Ollama (local) | `:11434` |
| Optional DB | Supabase (PostgreSQL) | — |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                CyberShield Console  (React, :8080)               │
│                                                                 │
│  /                      Home Page                               │
│  /scam-detection        URL / SMS / APK scanner                 │
│  /victim-assistance     LLM Chatbot for victims                 │
│  /awareness             Cyber-safety educational guides          │
│  /contact               Incident report form (→ Supabase)        │
│  /law-enforcement-console  Hidden: tap the navbar logo 5× in 2s  │
└───────────────────────────┬─────────────────────────────────────┘
                            │  HTTP / JSON (fetch)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               API Gateway  (FastAPI, :8000)                     │
│                                                                 │
│  GET  /api/transactions  → Block 1 → PaySim CSV → risk scores   │
│  POST /api/scan          → Block 2 → URL / text / APK scanners  │
│  POST /api/chat          → Block 3 → victim assistant chatbot   │
└──────┬──────────────────┬────────────────────┬──────────────────┘
       ▼                  ▼                    ▼
┌──────────────┐  ┌──────────────────┐  ┌────────────────────┐
│   Block 1    │  │    Block 2       │  │   Block 3          │
│ Transaction  │  │  Phishing /      │  │  Victim Assistant  │
│ Risk Engine  │  │  Malware Scanner │  │  (LLM Chatbot)     │
│ PyTorch AE + │  │  RF + heuristics │  │                    │
│ rules        │  │                  │  │                    │
└──────────────┘  └──────────────────┘  └──────────┬─────────┘
                                                   ▼
                                        ┌────────────────────┐
                                        │  Ollama            │
                                        │  http://127.0.0.1 │
                                        │  :11434 llama3     │
                                        └────────────────────┘
```

---

## Project Flow — End to End

### 1. Scam Detection (`/scam-detection`)

Frontend hits `POST http://localhost:8000/api/scan` with `{ type: "url" | "message", content }`.

1. **API Gateway** routes to `analyze_url()` or `analyze_text()` in **Block 2**.
2. Feature extraction produces numerical features (10 for URLs, 8 for text).
3. A heuristic rule engine scores the content, and a Random Forest model predicts fraud probability.
4. The two are blended into a **hybrid score** (weighted combination).
5. Score → risk verdict: `high` (>70) / `medium` (>40) / `low`.
6. For `high`/`medium`, the gateway asks **Ollama/LLaMA 3** to generate a short human-readable explanation (XAI).
7. Frontend renders the **RiskBadge** (Low/Medium/High) + explanation + recommended actions.

```
User pastes URL/message  →  POST /api/scan  →  Slock 2 scanner
        ←  { risk, explanation, recommendations[] }  ←  Ollama XAI
```

### 2. Victim Assistance (`/victim-assistance`)

Frontend hits `POST http://localhost:8000/api/chat` with `{ message }`.

1. **Block 3** `chatbot_manager.get_response()` first checks the input with `intent_detector` — only cyber-safety topics are accepted (boundary enforcement).
2. `language_style` detects English / Tamil / Tanglish and adapts tone.
3. An empathetic opening phrase is generated (`reassurance`).
4. The prompt + `system_prompt.txt` persona is sent to **Ollama LLaMA 3**.
5. A safety footer is appended (never share OTP/PIN, call 1930, visit cybercrime.gov.in).
6. Frontend appends the reply as a chat bubble.

### 3. Law Enforcement Console (hidden route)

Why hidden: the console is *not* linked in the navbar — access it by **clicking the CyberShield logo 5 times within 2 seconds** (`Navbar.tsx`).

Frontend hits `GET http://localhost:8000/api/transactions`.

1. Gateway samples 10 rows from the **PaySim dataset** (`block1_transaction_engine/paysim dataset.csv`), falling back to `sample_transactions.csv`.
2. **Block 1** `calculate_hybrid_risk()` runs:
   - `extract_features()` → 11 aggregated features per account.
   - `RuleEngine` → heuristic fraud score (0–90) from 4 rules (sudden spike, quick in/out, many recipients, multiple devices).
   - PyTorch **Autoencoder** → per-account reconstruction-error anomaly scores.
   - Feature contributions (top anomalous features) → XAI `anomaly_reason`.
3. `hybrid_score = 0.6 × rule_score + 0.4 × ml_score_normalized`.
4. Risk threshold: `>60` HIGH · `30–60` MEDIUM · `<30` LOW.
5. Frontend renders a filterable table with RiskBadges, scores, and anomaly reasons.

```
GET /api/transactions → PaySim sample → feature extraction
        → RuleEngine + Autoencoder → hybrid score → JSON table
```

### 4. Incident Reporting (`/contact`)

Form validates, then writes directly to **Supabase** `public.reports` table (insert-only policy) and shows a success state. `.env` supplies the Supabase keys.

### 5. Awareness (`/awareness`) and Home (`/`)

Static pages — educational content and feature cards linking to the tools above.

---

## Directory Structure

```
CSH__VisionX/
│
├── api_gateway.py                    # FastAPI gateway bundling all blocks (port 8000)
├── README.md                         # This file
├── CYBERSHIELD_DOCUMENTATION.md      # Full detailed documentation
│
├── block1_transaction_engine/        # Fraud transaction risk engine
│   ├── hybrid_risk.py                #   Hybrid scorer (rules + autoencoder)
│   ├── rules.py                      #   Heuristic RuleEngine (4 fraud rules)
│   ├── sample_transactions.csv       #   Small fallback dataset
│   ├── ae_model_v2.pth / ae_scaler_v2.pkl  # Trained model artifacts
│   └── ml_model/                     #   PyTorch Autoencoder + feature pipeline
│
├── block2_phishing_scanner/          # URL / SMS / APK threat scanners
│   ├── url_scanner/                  #   URL features, rules, hy brid scorer
│   ├── text_scanner/                 #   NLP features, message model, rules
│   ├── malware_scanner/              #   APK hash + static analysis
│   └── *.pkl                         #   Trained Random Forest models
│
├── block3_victim_assistant/          # LLM chatbot for victims
│   ├── chatbot_manager.py            #   Orchestrates the full response pipeline
│   ├── intent_detector.py            #   Boundary enforcement
│   ├── language_style.py             #   English / Tamil / Tanglish
│   ├── reassurance.py                #   Empathetic openers
│   ├── llm_engine.py                 #   Ollama REST caller
│   └── system_prompt.txt             #   LLM persona
│
└── cybershield-console/              # React frontend (port 8080)
    ├── src/pages/                    #   Home, ScamDetection, VictimAssistance,
    │                                 #   Awareness, Contact, LawEnforcementConsole
    ├── src/components/               #   Navbar, Layout, RiskBadge, shadcn/ui
    ├── src/integrations/supabase/    #   Supabase client + types
    ├── supabase/migrations/          #   SQL: reports + le_transactions tables
    └── package.json
```

> `paysim dataset.csv` (~470 MB) is **not** committed to GitHub (exceeds the 100 MB limit) — it stays local and is `.gitignore`d. The gateway auto-falls back to `sample_transactions.csv` when it is absent, and Block 1 auto-trains a fresh Autoencoder if the model files are missing.

---

## Running the System

### Prerequisites

- Python 3.11+ with the packages: `fastapi uvicorn pydantic pandas numpy torch scikit-learn scipy joblib requests tldextract validators`
- Node 18+ (for the frontend)
- Ollama with `llama3` pulled — required for the chatbot and XAI explanations

### 1. Start the backend (Terminal A)

```powershell
cd CSH__VisionX
python api_gateway.py
# API at http://localhost:8000  (interactive docs: /docs)
```

### 2. Configure the frontend

Set the real values in `cybershield-console/.env` (the committed file has placeholders):

```
VITE_SUPABASE_URL=<your-project-url>
VITE_SUPABASE_PUBLISHABLE_KEY=<your-anon-key>
```

### 3. Start the frontend (Terminal B)

```powershell
cd CSH__VisionX/cybershield-console
npm install
npm run dev
# UI at http://localhost:8080
```

### 4. Optional — train the transaction model

```powershell
cd block1_transaction_engine
python train_model.py        # writes ae_model_v2.pth + ae_scaler_v2.pkl
```

---

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Router, TanStack Query, Lucide
- **Backend:** Python, FastAPI, Uvicorn, Pandas, NumPy
- **ML:** PyTorch (Autoencoder), scikit-learn (Random Forest, scalers), joblib
- **LLM:** LLaMA 3 (8B) via local Ollama
- **Database:** Supabase (PostgreSQL, RLS-enabled)

---

## Security Notes

- `.env` is git-ignored — **never commit real API keys**. The currently committed placeholder must be replaced with your real Supabase key locally, and any previously leaked key should be rotated in the Supabase dashboard.
- The Law Enforcement Console has **no real authentication** — access is hidden behind the 5-tap logo gesture but is not a security boundary.
- The API Gateway uses open CORS and no API keys, suitable for local development only.