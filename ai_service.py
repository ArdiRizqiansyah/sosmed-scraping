import requests
import json
import re
from typing import List, Dict, Any

OPENROUTER_API_KEY = "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"

# Fast responding free models first, then user ultra model
AI_MODELS = [
    "minimax/minimax-m3:free",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free"
]

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "SosmedPulse Listening"
}

def generate_ai_sentiment_and_insights(keyword: str, items: List[Dict[str, Any]], stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Menggunakan OpenRouter LLM untuk menganalisis kumpulan percakapan produk secara holistik:
    - Menghasilkan ringkasan eksekutif mendalam (Executive Summary).
    - Mengekstrak pemicu sentimen positif spesifik (Product Strengths).
    - Mengekstrak keluhan/kritik konsumen spesifik (Pain Points / Complaints).
    - Memberikan rekomendasi bisnis strategis (Actionable Advice).
    """
    if not items:
        return None

    sample_snippets = []
    for i, it in enumerate(items[:8]):
        title = it.get('title', '')
        content = it.get('content', '')
        src = it.get('source', '')
        sample_snippets.append(f"- ({src}) {title}: {content}")
    
    text_corpus = "\n".join(sample_snippets)

    prompt = f"""Kamu adalah analis social media listening dan sentimen konsumen.
Analisis data percakapan publik media sosial berikut untuk brand/produk: "{keyword}".

Data Percakapan:
{text_corpus}

Statistik:
Total: {stats.get('total', len(items))}, Positif: {stats.get('pos_pct', 0)}%, Netral: {stats.get('neu_pct', 0)}%, Negatif: {stats.get('neg_pct', 0)}%, NSS: {stats.get('nss', 0)}

Berikan respon HANYA format JSON valid berikut (tanpa markdown tambahan):
{{
  "summary": "2 kalimat ringkasan sentimen dan persepsi warganet tentang {keyword}",
  "pos_drivers": ["poin kelebihan 1", "poin kelebihan 2"],
  "neg_drivers": ["poin keluhan 1", "poin keluhan 2"],
  "recommendation": "1 kalimat saran strategis untuk pemilik brand {keyword}"
}}"""

    for model in AI_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300,
            "temperature": 0.2
        }
        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=payload, timeout=5)
            if res.status_code == 200:
                raw_content = res.json()["choices"][0]["message"]["content"]
                json_match = re.search(r"\{.*\}", raw_content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group(0))
                    model_display = "Nemotron AI" if "nemotron" in model else "Minimax AI"
                    return {
                        "ai_summary": parsed.get("summary", ""),
                        "pos_drivers": parsed.get("pos_drivers", []),
                        "neg_drivers": parsed.get("neg_drivers", []),
                        "recommendation": parsed.get("recommendation", ""),
                        "model_used": model_display
                    }
        except Exception as e:
            continue

    return None
