import re
from collections import Counter
from typing import List, Dict, Any
import ai_service

POSITIVE_WORDS = {
    "bagus", "keren", "mantap", "mantul", "mantep", "puas", "suka", "terbaik",
    "top", "recommended", "rekomendasi", "juara", "hebat", "berkualitas", "premium",
    "original", "asli", "awet", "mulus", "canggih", "inovatif", "estetik",
    "aesthetic", "rapi", "rapih", "wangi", "lembut", "enak", "lezat", "nyaman",
    "worth", "worthit", "terjangkau", "murah", "hemat", "ekonomis", "cuan",
    "profit", "untung", "cepat", "responsif", "lancar", "ngebut", "kencang",
    "love", "senang", "gokil", "jos", "ciamik", "favorit", "solutif",
    "membantu", "berguna", "bermanfaat", "kece", "oke", "ok", "sukses",
    "naik", "tumbuh", "bangga", "terpercaya", "amanah", "sesuai", "cocok",
    "pas", "aman", "stabil", "konsisten", "packing", "packaging", "ramah",
    "fast respon", "fast response", "sigap", "profesional", "baik", "helpful",
    "repeat order", "repurchase", "langganan", "loyal", "puas banget",
    "recommended bgt", "rekomen", "terbukti", "nyata"
}

NEGATIVE_WORDS = {
    "jelek", "buruk", "rusak", "cacat", "palsu", "kw", "fake",
    "ancur", "hancur", "zonk", "ampas", "payah", "parah", "lemot",
    "lambat", "lelet", "boros", "cepat panas", "panas", "overheat",
    "mahal", "kemahalan", "rugi", "sayang uang", "tipu", "penipuan",
    "scam", "bohong", "php", "kecewa", "menyesal", "nyesal", "kapok",
    "tidak sesuai", "ga sesuai", "beda foto", "beda deskripsi",
    "tidak worth", "ga worth", "gak worth", "tidak recommended",
    "error", "bug", "crash", "freeze", "lag", "gagal", "drop",
    "tidak berfungsi", "mati", "bocor", "pecah", "slow respon",
    "tidak responsif", "lama balas", "tidak ramah", "kasar", "pengiriman lama",
    "telat", "terlambat", "tidak sampai", "hilang", "kecewa berat",
    "kecewa banget", "tidak puas", "ga puas", "gak puas", "tidak bagus",
    "ga bagus", "gak bagus", "jangan beli", "hindari", "tidak cocok"
}

NEGATION_WORDS = {
    "tidak", "tak", "bukan", "jangan", "gak", "ga", "nggak",
    "ndak", "tdk", "kurang", "belum", "bukanlah", "tanpa"
}

INTENSIFIER_WORDS = {
    "sangat", "banget", "bgt", "amat", "sekali", "super", "luar biasa",
    "parah", "beneran", "pol", "paling", "bener-bener", "sungguh",
    "terlalu", "begitu", "benar-benar"
}

INDONESIAN_STOPWORDS = {
    "dan", "di", "ke", "dari", "yang", "ini", "itu", "untuk", "pada", "adalah",
    "sebagai", "dengan", "ada", "bisa", "akan", "juga", "saya", "kami", "kita",
    "kamu", "anda", "mereka", "dia", "ia", "atau", "karena", "oleh", "dalam",
    "saat", "sudah", "telah", "sedang", "lebih", "banyak", "hanya", "tentang",
    "seperti", "antara", "namun", "tetapi", "jika", "bila", "apabila", "secara",
    "hingga", "sampai", "dapat", "harus", "lagi", "pun", "jadi", "kalo", "kalau",
    "nih", "deh", "dong", "sih", "kan", "lah", "ya", "aja", "saja", "kok",
    "para", "hal", "tersebut", "buat", "bikin", "mau", "ingin", "tahu", "tau",
    "hari", "tahun", "bulan", "waktu", "baca", "lengkap", "klik", "link", "video",
    "berita", "news", "com", "co", "id", "www", "https", "http", "via", "vs",
    "nya", "mu", "ku", "si", "sang", "tiap", "setiap", "seluruh", "semua",
    "cari", "lihat", "temukan", "buka", "terkait", "seputar", "mengenai"
}

# Kamus Kata Kunci Aspek Produk (Aspect-Based Sentiment)
ASPECT_KEYWORDS = {
    "kualitas": {
        "kualitas", "performa", "fitur", "hasil", "efek", "tekstur", "formula",
        "awet", "mulus", "rusak", "cacat", "lemot", "canggih", "bagus", "jelek",
        "ancur", "original", "asli", "palsu", "kw", "kamera", "baterai", "layar",
        "daya tahan", "bahan", "rasa", "enak", "wangi"
    },
    "harga": {
        "harga", "biaya", "tarif", "promo", "diskon", "murah", "mahal", "terjangkau",
        "hemat", "ekonomis", "kemahalan", "worth", "worthit", "cuan", "rugi",
        "price", "cashback", "anggaran"
    },
    "pengiriman": {
        "pengiriman", "ekspedisi", "kurir", "kirim", "sampai", "antar", "packing",
        "packaging", "kemasan", "box", "bubble wrap", "penyok", "pecah", "bocor",
        "telat", "terlambat", "cepat sampai", "kilat", "lama sampai"
    },
    "layanan": {
        "layanan", "service", "admin", "cs", "customer service", "seller", "penjual",
        "toko", "respon", "responsif", "ramah", "sigap", "fast respon", "slow respon",
        "kasar", "garansi", "after sales", "konsultasi", "komplain", "bantuan"
    }
}

# Kata Kunci Risiko Krisis Reputasi (PR Crisis Alert)
CRISIS_KEYWORDS = {
    "penipuan", "scam", "palsu", "ilegal", "berbahaya", "tipu", "bohong",
    "bocor", "rusak parah", "somasi", "lapor polisi", "tuntut", "rugi besar",
    "php", "korban", "racun", "kadaluarsa", "expired", "batal sepihak"
}

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"http\S+|www\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def analyze_sentiment(text: str) -> Dict[str, Any]:
    cleaned = clean_text(text).lower()
    words = cleaned.split()

    pos_score = 0.0
    neg_score = 0.0
    detected_pos = []
    detected_neg = []

    i = 0
    while i < len(words):
        word = words[i]
        bigram = f"{words[i-1]} {word}" if i > 0 else ""

        is_negated = (
            (i > 0 and words[i-1] in NEGATION_WORDS) or
            (i > 1 and words[i-2] in NEGATION_WORDS)
        )
        multiplier = 1.0
        if (i > 0 and words[i-1] in INTENSIFIER_WORDS) or \
           (i < len(words)-1 and words[i+1] in INTENSIFIER_WORDS):
            multiplier = 1.8

        target = bigram if bigram in POSITIVE_WORDS or bigram in NEGATIVE_WORDS else word

        if target in POSITIVE_WORDS:
            if is_negated:
                neg_score += 1.2 * multiplier
                detected_neg.append(f"tidak {target}")
            else:
                pos_score += 1.0 * multiplier
                detected_pos.append(target)
        elif target in NEGATIVE_WORDS:
            if is_negated:
                pos_score += 0.8 * multiplier
                detected_pos.append(f"tidak {target}")
            else:
                neg_score += 1.0 * multiplier
                detected_neg.append(target)

        i += 1

    total = pos_score + neg_score + 0.001
    if pos_score > neg_score and (pos_score - neg_score) >= 0.5:
        label = "Positif"
        score = min(100, int(((pos_score - neg_score) / total) * 100))
    elif neg_score > pos_score and (neg_score - pos_score) >= 0.5:
        label = "Negatif"
        score = max(-100, int(((pos_score - neg_score) / total) * 100))
    else:
        label = "Netral"
        score = 0

    return {
        "label": label,
        "score": score,
        "pos_words": list(set(detected_pos)),
        "neg_words": list(set(detected_neg))
    }

def extract_aspect_sentiment(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Menghitung sentimen spesifik pada 4 Aspek Bisnis:
    1. Kualitas & Fitur Produk
    2. Harga & Nilai (Value for Money)
    3. Pengiriman & Kemasan
    4. Layanan Pelanggan (CS)
    """
    aspect_counts = {
        "kualitas": {"pos": 0, "neg": 0, "total": 0},
        "harga": {"pos": 0, "neg": 0, "total": 0},
        "pengiriman": {"pos": 0, "neg": 0, "total": 0},
        "layanan": {"pos": 0, "neg": 0, "total": 0}
    }

    for it in items:
        text_lower = f"{it.get('title', '')} {it.get('content', '')}".lower()
        sentiment = it.get("sentiment", "Netral")

        for aspect_name, keywords in ASPECT_KEYWORDS.items():
            if any(k in text_lower for k in keywords):
                aspect_counts[aspect_name]["total"] += 1
                if sentiment == "Positif":
                    aspect_counts[aspect_name]["pos"] += 1
                elif sentiment == "Negatif":
                    aspect_counts[aspect_name]["neg"] += 1

    aspect_results = {}
    for aspect_name, data in aspect_counts.items():
        total = data["total"]
        if total > 0:
            pos_rate = round((data["pos"] / total) * 100)
            if pos_rate >= 70:
                status = "Sangat Baik"
                status_color = "emerald"
            elif pos_rate >= 40:
                status = "Cukup Baik"
                status_color = "indigo"
            else:
                status = "Perlu Evaluasi"
                status_color = "rose"
        else:
            pos_rate = 50
            status = "Netral / Stabil"
            status_color = "slate"

        aspect_results[aspect_name] = {
            "mentions": total,
            "pos_rate": pos_rate,
            "status": status,
            "status_color": status_color
        }

    return aspect_results

def detect_crisis_alerts(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Mendeteksi potensi krisis reputasi (PR Crisis) dari kemunculan kata-kata bahaya.
    """
    risk_counter = Counter()
    total_risk_mentions = 0

    for it in items:
        text_lower = f"{it.get('title', '')} {it.get('content', '')}".lower()
        for ck in CRISIS_KEYWORDS:
            if ck in text_lower:
                risk_counter[ck] += 1
                total_risk_mentions += 1

    if total_risk_mentions >= 3:
        status = "Peringatan Krisis Tinggi"
        level = "danger"
        color = "rose"
        advice = "Ditemukan beberapa indikasi komplain kritis. Segera lakukan klarifikasi publik atau koordinasi tim CS/PR."
    elif total_risk_mentions >= 1:
        status = "Waspada / Perlu Perhatian"
        level = "warning"
        color = "amber"
        advice = "Terdapat indikasi komplain spesifik dari konsumen. Pantau dan tanggapi secara persuasif."
    else:
        status = "Aman / Bebas Isu Kritis"
        level = "safe"
        color = "emerald"
        advice = "Tidak terdeteksi isu penipuan, bahaya produk, atau krisis reputasi yang signifikan."

    top_risks = [f"{w} ({c}x)" for w, c in risk_counter.most_common(4)]

    return {
        "status": status,
        "level": level,
        "color": color,
        "risk_count": total_risk_mentions,
        "top_risks": top_risks,
        "advice": advice
    }

def extract_keywords(texts: List[str], target_keyword: str, top_n: int = 25) -> List[Dict[str, Any]]:
    word_counter = Counter()
    target_tokens = set(target_keyword.lower().split())
    for text in texts:
        cleaned = clean_text(text).lower()
        for token in cleaned.split():
            if (len(token) > 2
                    and token not in INDONESIAN_STOPWORDS
                    and token not in target_tokens
                    and not token.isnumeric()):
                word_counter[token] += 1
    return [{"text": w, "value": c} for w, c in word_counter.most_common(top_n)]

def generate_local_summary(
    keyword: str, total: int,
    pos_pct: float, neg_pct: float, neu_pct: float,
    nss: float,
    top_keywords: List[Dict[str, Any]],
    top_pos_words: List[str],
    top_neg_words: List[str]
) -> str:
    kw_list = ", ".join([k["text"] for k in top_keywords[:6]]) or "berbagai aspek produk"
    if nss > 30:
        vibe = "sangat positif — brand ini menikmati respon baik dari konsumen"
    elif nss > 10:
        vibe = "cukup positif dan relatif stabil di ruang publik"
    elif nss > -10:
        vibe = "netral dan berimbang antara ulasan objektif dan diskusi umum"
    else:
        vibe = "cenderung negatif dengan sejumlah keluhan yang perlu dievaluasi"

    pos_str = f"Pujian konsumen dominan pada: **{', '.join(top_pos_words[:4])}**." if top_pos_words else "Belum ada pujian dominan yang spesifik."
    neg_str = f"Sorotan keluhan atau kritik: **{', '.join(top_neg_words[:4])}**." if top_neg_words else "Tidak ditemukan gelombang kritik negatif yang signifikan."

    return (
        f"Berdasarkan {total} percakapan publik yang dipantau, respon terhadap '{keyword}' saat ini berstatus {vibe} "
        f"(Net Sentiment Score: {nss:+.1f}). Topik yang paling sering diasosiasikan meliputi: {kw_list}. "
        f"{pos_str} {neg_str}"
    )

def analyze_dataset(keyword: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not items:
        return {
            "keyword": keyword,
            "total_mentions": 0,
            "sentiment_counts": {"Positif": 0, "Netral": 0, "Negatif": 0},
            "sentiment_percentages": {"Positif": 0, "Netral": 0, "Negatif": 0},
            "net_sentiment_score": 0,
            "top_keywords": [],
            "top_positive_drivers": [],
            "top_negative_drivers": [],
            "aspect_sentiments": {
                "kualitas": {"mentions": 0, "pos_rate": 50, "status": "Stabil", "status_color": "slate"},
                "harga": {"mentions": 0, "pos_rate": 50, "status": "Stabil", "status_color": "slate"},
                "pengiriman": {"mentions": 0, "pos_rate": 50, "status": "Stabil", "status_color": "slate"},
                "layanan": {"mentions": 0, "pos_rate": 50, "status": "Stabil", "status_color": "slate"}
            },
            "crisis_alert": {
                "status": "Aman", "level": "safe", "color": "emerald", "risk_count": 0, "top_risks": [],
                "advice": "Belum ada data percakapan."
            },
            "ai_summary": f"Belum ditemukan percakapan publik untuk keyword '{keyword}'. Silakan cek tautan eksplorasi langsung di bawah.",
            "ai_recommendation": "Coba gunakan kata kunci variasi atau pantau kembali saat produk mulai ramai diperbincangkan.",
            "engine_badge": "Hybrid NLP",
            "items": []
        }

    analyzed_items = []
    pos_count = neu_count = neg_count = 0
    all_pos_words = Counter()
    all_neg_words = Counter()
    all_texts = []

    for item in items:
        full_text = f"{item.get('title', '')} {item.get('content', '')}"
        result = analyze_sentiment(full_text)

        if result["label"] == "Positif":
            pos_count += 1
        elif result["label"] == "Negatif":
            neg_count += 1
        else:
            neu_count += 1

        for w in result["pos_words"]:
            all_pos_words[w] += 1
        for w in result["neg_words"]:
            all_neg_words[w] += 1

        all_texts.append(full_text)
        analyzed_items.append({
            **item,
            "sentiment": result["label"],
            "sentiment_score": result["score"]
        })

    total = len(items)
    pos_pct = round((pos_count / total) * 100, 1)
    neu_pct = round((neu_count / total) * 100, 1)
    neg_pct = round((neg_count / total) * 100, 1)
    nss = round(pos_pct - neg_pct, 1)

    top_keywords = extract_keywords(all_texts, keyword, top_n=25)
    local_pos_drivers = [w for w, _ in all_pos_words.most_common(6)]
    local_neg_drivers = [w for w, _ in all_neg_words.most_common(6)]

    # 1. Hitung Aspect-Based Sentiment (4 Pilar Bisnis)
    aspect_sentiments = extract_aspect_sentiment(analyzed_items)

    # 2. Deteksi Krisis Reputasi (PR Crisis Alert)
    crisis_alert = detect_crisis_alerts(analyzed_items)

    stats = {
        "total": total,
        "pos_pct": pos_pct,
        "neu_pct": neu_pct,
        "neg_pct": neg_pct,
        "nss": nss
    }

    # 3. Panggil OpenRouter AI untuk analisis mendalam
    ai_result = ai_service.generate_ai_sentiment_and_insights(keyword, items, stats)

    if ai_result:
        ai_summary = ai_result.get("ai_summary", "") or generate_local_summary(keyword, total, pos_pct, neg_pct, neu_pct, nss, top_keywords, local_pos_drivers, local_neg_drivers)
        ai_rec = ai_result.get("recommendation", "")
        pos_drivers = ai_result.get("pos_drivers") or local_pos_drivers
        neg_drivers = ai_result.get("neg_drivers") or local_neg_drivers
        engine_badge = f"OpenRouter AI ({ai_result.get('model_used', 'Nemotron')})"
    else:
        ai_summary = generate_local_summary(keyword, total, pos_pct, neg_pct, neu_pct, nss, top_keywords, local_pos_drivers, local_neg_drivers)
        ai_rec = "Pertahankan kepuasan pelanggan dan terus pantau sentimen produk secara berkala."
        pos_drivers = local_pos_drivers
        neg_drivers = local_neg_drivers
        engine_badge = "Indonesian NLP Lexicon"

    return {
        "keyword": keyword,
        "total_mentions": total,
        "sentiment_counts": {"Positif": pos_count, "Netral": neu_count, "Negatif": neg_count},
        "sentiment_percentages": {"Positif": pos_pct, "Netral": neu_pct, "Negatif": neg_pct},
        "net_sentiment_score": nss,
        "top_keywords": top_keywords,
        "top_positive_drivers": pos_drivers,
        "top_negative_drivers": neg_drivers,
        "aspect_sentiments": aspect_sentiments,
        "crisis_alert": crisis_alert,
        "ai_summary": ai_summary,
        "ai_recommendation": ai_rec,
        "engine_badge": engine_badge,
        "items": analyzed_items
    }
