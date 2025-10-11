from transformers import pipeline
import re
import json
from typing import List, Dict, Any
from openai import OpenAI

def metni_temizle(metin: str) -> str:
    metin = re.sub(r'\s+', ' ', metin)
    return metin.strip()

def ozel_tokenlari_temizle(metin: str) -> str:
    metin = re.sub(r'<extra_id_\d+>', '', metin)
    metin = re.sub(r'<pad>|</s>|<unk>|<s>', '', metin)
    metin = re.sub(r'\(\s*\)|"\s*"|\'\s*\'', '', metin)
    metin = re.sub(r'\.+', '.', metin)
    metin = re.sub(r',+', ',', metin)
    metin = re.sub(r'\s+([.,;:!?])', r'\1', metin)
    metin = re.sub(r'\s+', ' ', metin)
    return metin.strip()

def cumlelerine_ayir(metin: str) -> list:
    cumleler = re.split(r'(?<=[.!?])\s+', metin)
    cumleler = [c.strip() for c in cumleler if len(c.strip()) > 20 and len(c.split()) > 3]
    return cumleler

def benzerlik_skoru(cumle1: str, cumle2: str) -> float:
    kelimeler1 = set(cumle1.lower().split())
    kelimeler2 = set(cumle2.lower().split())
    if not kelimeler1 or not kelimeler2:
        return 0
    kesisim = len(kelimeler1.intersection(kelimeler2))
    birlesim = len(kelimeler1.union(kelimeler2))
    return kesisim / birlesim if birlesim > 0 else 0

def metin_kalitesi_kontrol(metin: str) -> bool:
    if not metin or len(metin.strip()) < 10 or len(metin.split()) < 3:
        return False
    ozel_karakter_orani = len(re.findall(r'[<>{}[\]]', metin)) / len(metin)
    if ozel_karakter_orani > 0.1:
        return False
    return True

def benzersiz_ozetleri_sec(ozetler: list, esik: float = 0.5) -> list:
    if not ozetler:
        return []
    temiz_ozetler = []
    for ozet in ozetler:
        if not metin_kalitesi_kontrol(ozet):
            continue
        benzer_var = False
        for mevcut in temiz_ozetler:
            if benzerlik_skoru(ozet, mevcut) > esik:
                benzer_var = True
                break
        if not benzer_var:
            temiz_ozetler.append(ozet)
    return temiz_ozetler

def cumlelerden_tekrarlari_kaldir(metin: str) -> str:
    cumleler = re.split(r'(?<=[.!?])\s+', metin)
    benzersiz_cumleler = []
    for cumle in cumleler:
        cumle = cumle.strip()
        if not cumle:
            continue
        benzer_var = False
        for mevcut in benzersiz_cumleler:
            if benzerlik_skoru(cumle, mevcut) > 0.6:
                benzer_var = True
                break
        if not benzer_var:
            benzersiz_cumleler.append(cumle)
    return ' '.join(benzersiz_cumleler)

def final_ozeti_olustur(benzersiz_ozetler: list) -> str:
    if not benzersiz_ozetler:
        return ""
    final_ozet = ' '.join(benzersiz_ozetler)
    final_ozet = ozel_tokenlari_temizle(final_ozet)
    final_ozet = cumlelerden_tekrarlari_kaldir(final_ozet)
    if final_ozet:
        final_ozet = final_ozet[0].upper() + final_ozet[1:]
    if final_ozet and final_ozet[-1] not in '.!?':
        final_ozet += '.'
    return final_ozet

def openai_ile_duzelt(ozet: str, api_key: str) -> str:
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sen Türkçe editörsün. Yazım hatalarını düzelt, tekrarları kaldır, metni akıcı yap. Sadece düzeltilmiş metni ver, açıklama yapma."
                },
                {
                    "role": "user",
                    "content": f"Düzelt:\n\n{ozet}"
                }
            ],
            temperature=0.2,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return ozet

def haber_ozetle(haber_icerigi: str, summarizer: Any, openai_api_key: str) -> Dict[str, Any]:
    if not haber_icerigi:
        return {"ozet": "", "orijinal_kelime_sayisi": 0, "ozet_kelime_sayisi": 0}
    
    haber = metni_temizle(haber_icerigi)
    cumleler = cumlelerine_ayir(haber)
    
    if not cumleler:
        return {"ozet": "", "orijinal_kelime_sayisi": len(haber.split()), "ozet_kelime_sayisi": 0}
    
    basarili_ozetler = []
    for cumle in cumleler:
        try:
            ozet_sonuc = summarizer(
                cumle,
                max_length=60,
                min_length=15,
                do_sample=False,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            ozet_metin = ozel_tokenlari_temizle(ozet_sonuc[0].get('summary_text', ''))
            if metin_kalitesi_kontrol(ozet_metin):
                basarili_ozetler.append(ozet_metin)
        except Exception:
            continue
    
    if not basarili_ozetler:
        return {"ozet": "", "orijinal_kelime_sayisi": len(haber.split()), "ozet_kelime_sayisi": 0}
    
    benzersiz_ozetler = benzersiz_ozetleri_sec(basarili_ozetler, esik=0.5)
    final_ozet = final_ozeti_olustur(benzersiz_ozetler)
    
    if not final_ozet:
        return {"ozet": "", "orijinal_kelime_sayisi": len(haber.split()), "ozet_kelime_sayisi": 0}
    
    duzeltilmis_ozet = openai_ile_duzelt(final_ozet, openai_api_key)
    
    return {
        "ozet": duzeltilmis_ozet,
        "orijinal_kelime_sayisi": len(haber.split()),
        "ozet_kelime_sayisi": len(duzeltilmis_ozet.split())
    }

def toplu_ozetle(haberler: List[Dict[str, Any]], summarizer: Any, openai_api_key: str) -> List[Dict[str, Any]]:
    sonuclar = []
    toplam = len(haberler)
    
    for idx, haber_data in enumerate(haberler, 1):
        print(f"[{idx}/{toplam}] İşleniyor...")
        
        haber_icerigi = haber_data.get("haberIcerigi", "")
        ozet_bilgileri = haber_ozetle(haber_icerigi, summarizer, openai_api_key)
        
        sonuc = {
            "haberBasligi": haber_data.get("haberBasligi", ""),
            "haberIcerigi": haber_data.get("haberIcerigi", ""),
            "haberGorseli": haber_data.get("haberGorseli", ""),
            "haberTarihi": haber_data.get("haberTarihi", ""),
            "haberKategorisi": haber_data.get("haberKategorisi", ""),
            "haberOzeti": ozet_bilgileri["ozet"],
            "orijinal_kelime_sayisi": ozet_bilgileri["orijinal_kelime_sayisi"],
            "ozet_kelime_sayisi": ozet_bilgileri["ozet_kelime_sayisi"]
        }
        
        sonuclar.append(sonuc)
    
    return sonuclar

if __name__ == "__main__":
    
    OPENAI_API_KEY = your_api_key"
    # JSON dosyasını yükle
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            haberler = json.load(file)
        print(f"{len(haberler)} haber yüklendi.\n")
    except Exception as e:
        print(f"Hata: data.json yüklenemedi. {e}")
        exit(1)
    
    # Model yükle
    print("Model yükleniyor...")
    try:
        summarizer = pipeline(
            "summarization",
            model="nicktimur/mt5-base-turkish-news-summarizer",
            tokenizer="nicktimur/mt5-base-turkish-news-summarizer",
            device=-1
        )
        print("Model yüklendi.\n")
    except Exception as e:
        print(f"Hata: Model yüklenemedi. {e}")
        exit(1)
    
    # Toplu özetleme
    print("Özetleme başlıyor...\n")
    sonuclar = toplu_ozetle(haberler, summarizer, OPENAI_API_KEY)
    
    # Sonuçları kaydet
    with open("ozetlenmis_haberler.json", "w", encoding="utf-8") as file:
        json.dump(sonuclar, file, indent=4, ensure_ascii=False)
    
    print(f"\n✓ Tamamlandı. Sonuçlar 'ozetlenmis_haberler.json' dosyasına kaydedildi.")
    print(f"\nÖrnek çıktı:")
    print(json.dumps(sonuclar[0], indent=4, ensure_ascii=False))
