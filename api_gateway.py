import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

# Add blocks to Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'block1_transaction_engine'))
sys.path.append(os.path.join(BASE_DIR, 'block2_phishing_scanner'))
sys.path.append(os.path.join(BASE_DIR, 'block3_victim_assistant'))

from block1_transaction_engine.hybrid_risk import calculate_hybrid_risk
from block2_phishing_scanner.url_scanner.hybrid_url_risk import analyze_url
from block2_phishing_scanner.text_scanner.hybrid_text_risk import analyze_text
from block2_phishing_scanner.malware_scanner.hybrid_apk_risk import analyze_apk
from block3_victim_assistant.chatbot_manager import get_response
import requests

app = FastAPI(title="CyberShield API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ScanRequest(BaseModel):
    type: str
    content: str

@app.get("/api/transactions")
def get_transactions():
    try:
        csv_path = os.path.join(BASE_DIR, 'block1_transaction_engine', 'paysim dataset.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path).sample(10, random_state=42)
        else:
            csv_path = os.path.join(BASE_DIR, 'block1_transaction_engine', 'sample_transactions.csv')
            df = pd.read_csv(csv_path)
            
        results = calculate_hybrid_risk(df)
        
        records = []
        for idx, row in results.iterrows():
            orig_row = df[df['sender_account'] == row['account']].iloc[0] if 'sender_account' in df.columns else None
            if orig_row is None and 'nameOrig' in df.columns:
                orig_row = df[df['nameOrig'] == row['account']].iloc[0]
            
            records.append({
                "id": str(idx),
                "accountId": row['account'],
                "riskScore": int(row['hybrid_score']),
                "riskLevel": row['risk_level'].lower(),
                "amount": float(orig_row['amount']) if orig_row is not None and 'amount' in orig_row else 0,
                "type": "Transfer",
                "source": "Account",
                "destination": orig_row['receiver_account'] if orig_row is not None and 'receiver_account' in orig_row else (orig_row['nameDest'] if orig_row is not None and 'nameDest' in orig_row else "Unknown"),
                "timestamp": str(orig_row['timestamp']) if orig_row is not None and 'timestamp' in orig_row else (str(orig_row['step']) if orig_row is not None and 'step' in orig_row else "Recent"),
                "anomaly_reason": row.get('anomaly_reason', '')
            })
        return records
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/api/scan")
def scan_content(request: ScanRequest):
    try:
        if request.type == 'url':
            result = analyze_url(request.content)
        elif request.type == 'file' or request.type == 'apk':
            # Support for APK scanning via absolute path
            result = analyze_apk(request.content)
        else:
            result = analyze_text(request.content)
            
        risk = result.get('verdict', 'SAFE').lower()
        hybrid_score = result.get('hybrid_score', 0)
        
        if risk in ["phishing", "scam", "malware", "malicious"]:
            risk = "high"
        elif risk == "suspicious":
            risk = "medium"
        else:
            risk = "low"

        # Dynamically generate explainability using local Ollama!
        llm_explanation = f"Analyzed by ML and Heuristics (Score: {hybrid_score})"
        try:
            if risk in ["high", "medium"]:
                prompt = f"Explain briefly why this {request.type} might be dangerous in 2 sentences. Content: {request.content}"
                resp = requests.post("http://127.0.0.1:11434/api/generate", json={
                    "model": "llama3:latest", "prompt": prompt, "stream": False, "options": {"temperature": 0.2}
                }, timeout=2)
                if resp.status_code == 200:
                    llm_explanation = resp.json().get("response", "").strip()
        except:
            pass # Fallback to default if LLM fails
            
        return {
            "risk": risk,
            "explanation": f"Score: {hybrid_score} - {llm_explanation}",
            "recommendations": [
                "Do not interact with this content." if risk == "high" else "Exercise caution.",
                "Report this to your IT administrator.",
                "Run a full system scan if you already clicked or downloaded."
            ] if risk in ["high", "medium"] else [
                "This content appears safe based on our models.",
                "Always verify the sender's identity.",
                "Keep your security software updated."
            ]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        response = get_response(request.message)
        return {"response": response}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
