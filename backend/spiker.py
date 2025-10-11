from flask import Flask, request, jsonify
from openai import OpenAI
import requests
import json, os, hashlib
from flask import Response
from dotenv import load_dotenv

# -----------------------------
# 🔑 API Keys
# -----------------------------
load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# 🔧 Flask App
# -----------------------------
app = Flask(__name__)

# Veriyi yükle
with open("ozetlenmis_data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

# -----------------------------
# 🧠 Yardımcı fonksiyonlar
# -----------------------------
def generate_spiker_text(kategori, ozetler):
    """GPT ile headline ve broadcast_text oluşturur, spiker tarzı ve ilgi çekici giriş ekler."""
    ozetler = ozetler[:10]  # En fazla 10 haber
    haber_listesi_str = "\n".join([f"{i+1}. {h}" for i, h in enumerate(ozetler)])
    haber_sayisi = len(ozetler)

    prompt = f"""
    Sen profesyonel bir haber spikerisin. {kategori.capitalize()} kategorisindeki haberleri sunuyorsun.
    Aşağıdaki {haber_sayisi} haberi oku ve her birini kapsayan, akıcı, ilgi çekici bir spiker metni oluştur.
    Hoş geldiniz cümlesi ile başla: 
    "Hoş geldiniz! Zaman tünelinde {kategori} dünyasına bakınca bu haberleri görüyoruz."

    Kurallar:
    - Türkçe yaz, doğal konuşma dili kullan.
    - JSON formatında döndür: {{"headline":"...","broadcast_text":"..."}}
    - headline: 7–10 kelimeyi geçmeyen kısa başlık.
    - broadcast_text: {haber_sayisi} cümlelik bir metin yaz. Her cümle, listedeki bir haberi özetlemeli ve tüm haberler mutlaka kapsanmalı.
    - Her haberi ayrı bir cümlede ele al, genelleme yapma.
    - Metin, profesyonel bir haber spikeri gibi akıcı ve enerjik olmalı.

    Haberler:
    {haber_listesi_str}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content.strip()

    # Kod bloğu varsa temizle
    if text.startswith("```json"):
        text = text[text.find("{"):text.rfind("}")+1]

    # JSON parse
    try:
        parsed = json.loads(text)
        headline = parsed.get("headline", "").strip()
        spiker_text = parsed.get("broadcast_text", "").strip()
    except Exception:
        fallback_text = text.replace("\n", " ").strip()
        headline = fallback_text[:80] + "..."
        spiker_text = fallback_text

    # Çıktıyı doğrula ve eksik haberleri ekle
    missing_news = validate_spiker_text(spiker_text, ozetler)
    if missing_news:
        spiker_text = append_missing_news(spiker_text, missing_news, kategori)

    return {"headline": headline, "broadcast_text": spiker_text}

def validate_spiker_text(spiker_text, ozetler):
    """Spiker metninin tüm haberleri kapsayıp kapsamadığını kontrol eder."""
    missing_news = []
    for ozet in ozetler:
        if ozet.lower() not in spiker_text.lower():
            missing_news.append(ozet)
    return missing_news

def append_missing_news(spiker_text, missing_news, kategori):
    """Eksik haberleri spiker metnine ekler."""
    if not missing_news:
        return spiker_text
    prompt = f"""
    Aşağıdaki spiker metnine, eksik olan haberleri akıcı bir şekilde ekle:
    Mevcut metin: {spiker_text}
    Eksik haberler: {', '.join(missing_news)}
    Türkçe yaz, doğal konuşma dili kullan ve profesyonel bir spiker tarzı koru.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

def generate_voice(metin, kategori):
    """ElevenLabs ile ses oluşturur."""
    os.makedirs("static/audio", exist_ok=True)
    hash_id = hashlib.md5(metin.encode()).hexdigest()[:10]
    filename = f"static/audio/{kategori}_{hash_id}.mp3"

    if os.path.exists(filename):
        return f"/{filename}"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": metin,
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.9}
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code != 200:
        print(f"ElevenLabs API hatası: {r.text}")
        return "/static/audio/fallback.mp3"  # Daha anlamlı bir varsayılan dosya

    with open(filename, "wb") as f:
        f.write(r.content)
    return f"/{filename}"

# -----------------------------
# 🧩 API Endpoint
# -----------------------------
@app.route("/api/spiker", methods=["GET"])
def spiker():
    kategori = request.args.get("kategori", "").lower()
    if not kategori:
        return jsonify({"error": "Kategori parametresi gerekli"}), 400

    ozetler = [
        h["ozet"] for h in DATA
        if h.get("original_data", {}).get("haberKategorisi", "").lower() == kategori
    ]
    if not ozetler:
        return jsonify({"error": f"{kategori} kategorisinde haber bulunamadı"}), 404

    # Spiker metni üret
    result = generate_spiker_text(kategori, ozetler)
    headline = result["headline"]
    spiker_text = result["broadcast_text"]

    # Ses üret
    audio_url = generate_voice(spiker_text, kategori)

    result = {
        "kategori": kategori,
        "headline": headline,
        "spiker_metin": spiker_text,
        "audio_url": audio_url
    }

    return Response(json.dumps(result, ensure_ascii=False), mimetype="application/json; charset=utf-8")

# -----------------------------
# 🚀 Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)