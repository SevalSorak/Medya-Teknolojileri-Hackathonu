
# Medya Teknolojileri Hackathonu Projesi

Bu proje, Medya Teknolojileri Hackathonu için geliştirilmiş bir haber zaman tüneli uygulamasıdır. Proje, geçmişten günümüze Anadolu Ajansı (AA) haberlerini toplayan, özetleyen ve bu haberlerden video kısa filmler üreten bir sistemden oluşmaktadır.

## Özellikler

- **Haber Toplama:** Anadolu Ajansı'nın RSS akışlarından ve Wayback Machine CDX API'si kullanılarak geçmişe dönük haberleri toplar.
- **Metin Özetleme:** Toplanan haber metinlerini, `nicktimur/mt5-base-turkish-news-summarizer` modeli ve OpenAI GPT-4 kullanarak özetler.
- **Video Oluşturma:** Belirtilen bir videodan, `faster-whisper` ile metin dökümü oluşturur, OpenAI GPT-4 ile önemli anları belirler ve `moviepy` kullanarak altyazılı kısa videolar oluşturur.
- **Metin Okuma (TTS):** ElevenLabs API'sini kullanarak verilen metni seslendirir.
- **Web Arayüzü:** Kullanıcıların belirli bir tarihe giderek o tarihteki haberleri görmelerini sağlayan "Haber Zaman Tüneli" adında bir web arayüzü sunar.

## Teknolojiler

- **Backend:**
    - Python
    - Flask
    - requests
    - BeautifulSoup
    - feedparser
    - transformers
    - faster-whisper
    - moviepy
    - openai
    - elevenlabs
- **Frontend:**
    - HTML
    - CSS
    - JavaScript

## Kurulum ve Kullanım

1.  **Proje Dosyalarını İndirin:**
    ```bash
    git clone https://github.com/kullanici/Medya-Teknolojileri-Hackathonu.git
    cd Medya-Teknolojileri-Hackathonu
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Not: `requirements.txt` dosyası projede bulunmamaktadır. Kullanılan kütüphaneler yukarıda listelenmiştir.)*

3.  **API Anahtarlarını Ayarlayın:**
    - `backend/summarized_data.py` dosyasında `OPENAI_API_KEY` değişkenine OpenAI API anahtarınızı girin.
    - `backend/generate_video_shorts.py` dosyasında `openai_api_key` değişkenine OpenAI API anahtarınızı girin.
    - `backend/voice.py` dosyasında `.env` dosyası oluşturarak `ELEVEN_API_KEY` ve `VOICE_ID` değişkenlerini ayarlayın.

4.  **Backend Betiklerini Çalıştırın:**
    - Haberleri toplamak için:
        ```bash
        python backend/aa_scraping.py
        python backend/rss_scraping.py
        ```
    - Haberleri özetlemek için:
        ```bash
        python backend/summarized_data.py
        ```
    - TTS sunucusunu başlatmak için:
        ```bash
        python backend/voice.py
        ```

5.  **Frontend'i Başlatın:**
    - `frontend/index.html` dosyasını bir web tarayıcısında açın.

## Dosya Açıklamaları

- **`backend/aa_scraping.py`**: Wayback Machine CDX API'sini kullanarak AA haberlerini kazır.
- **`backend/rss_scraping.py`**: AA RSS akışlarından haberleri kazır.
- **`backend/summarized_data.py`**: Haberleri özetler.
- **`backend/generate_video_shorts.py`**: Videolardan kısa filmler oluşturur.
- **`backend/voice.py`**: Metin okuma (TTS) için Flask API sunucusu.
- **`frontend/index.html`**: Ana sayfa, "Haber Zaman Tüneli".
- **`frontend/gallery.html`**: Belirli bir tarihteki haberlerin görüntülendiği galeri sayfası.
