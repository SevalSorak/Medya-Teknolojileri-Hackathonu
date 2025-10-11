# 📰 ANADOLU: HABER ZAMAN TÜNELİ  
### Medya Teknolojileri Hackathonu Projesi

Bu proje, kullanıcılara **Anadolu Ajansı (AA)** haberleri üzerinden interaktif bir **“zaman tüneli” deneyimi** sunan, kapsamlı bir web uygulamasıdır.  

Kullanıcılar, seçtikleri bir tarihe giderek o günün haberlerini **3D bir ortamda** keşfedebilir, haberleri **okuyabilir**, **yapay zeka destekli seslendirme** ile **dinleyebilir** ve hatta **haberlerden üretilmiş video özetlerini** izleyebilirler.  

Proje, güçlü bir **Python backend'i** ile etkileyici bir **three.js frontend'ini** bir araya getirerek, medya içeriklerini tüketmek için yenilikçi bir yol sunar.

---

## 🏛️ Sistem Mimarisi

Proje, iki ana bileşenden oluşur:

### Backend (Veri İşleme ve Servisler)
- **Veri Toplama**: AA'nın geçmiş ve güncel haberlerini toplamak için iki farklı yöntem kullanılır:
  - **Wayback Machine CDX API**: Arşivlenmiş haberlerin kazınması.
  - **RSS Akışları**: Güncel haberlerin periyodik olarak taranması.
- **Veri İşleme ve Özetleme**: 
  - Ham haber metinleri, **transformers** kütüphanesi ve `nicktimur/mt5-base-turkish-news-summarizer` modeli ile özetlenir.
  - Özetler, **OpenAI gpt-4o-mini** modeli ile daha akıcı ve okunabilir hale getirilir.
- **Video Oluşturma**: 
  - **ffmpeg**, **faster-whisper** ve **moviepy** kullanılarak videoların sesi metne dönüştürülür.
  - **gpt-4** ile önemli anlar belirlenir ve altyazılı kısa videolar (shorts) oluşturulur.
- **Text-to-Speech (TTS) API**: 
  - **Flask** ve **ElevenLabs API** kullanılarak metinler doğal insan sesine dönüştürülür.

### Frontend (Kullanıcı Arayüzü ve Deneyimi)
- **Ana Sayfa (index.html)**: 
  - Eski gazete tasarımına sahip estetik bir giriş sayfası.
  - Kullanıcıdan tarih seçimi alır ve seçilen tarihi `gallery.html` sayfasına aktarır.
- **3D Haber Galerisi (gallery.html)**:
  - **three.js** ile oluşturulmuş sürükleyici bir 3D sanat galerisi.
  - Seçilen tarihe ait haberler, galeri duvarlarında interaktif **kristal tablolara** dönüştürülür.
  - Kullanıcılar **W/A/S/D tuşları** ve **fare** ile galeride gezinebilir.
  - Her tabloya tıklandığında haberin detaylarını (başlık, görsel, tam metin) gösteren bir modal açılır.
  - Modal içindeki **“Seslendir” butonu**, backend’deki TTS API’sini kullanarak haber metnini sesli okur.
  - Galeri, kategoriye göre yorum yapan **NPC’ler** (Non-Player Characters) ile canlılık kazanır.
  - Ana salondan farklı haber kategorileri için özel odalara geçiş sağlayan kapılar bulunur.

---

## ✨ Temel Özellikler
- **İnteraktif 3D Deneyim**: Haberleri sıkıcı bir listede değil, gezilebilir bir 3D galeride keşfedin.
- **Yapay Zeka Destekli Özetleme**: Karmaşık haber metinleri, son teknoloji NLP modelleriyle kısa ve anlamlı özetlere dönüştürülür.
- **Otomatik Video “Shorts” Üretimi**: Videolardan en can alıcı kısımlar belirlenip sosyal medyaya uygun kısa videolar hazırlanır.
- **Doğal Seslendirme**: **ElevenLabs** entegrasyonu ile haber metinleri yüksek kaliteli ve doğal bir sesle dinlenir.
- **Dinamik Ortam**: Seçilen yılın ruhuna uygun değişen galeri temaları ve NPC’ler ile zenginleştirilmiş atmosfer.
- **Geçmişe Yolculuk**: **Wayback Machine** entegrasyonu ile geçmiş yıllara ait haberlere erişim.

---

## 🛠️ Kullanılan Teknolojiler

### Backend
- **Dil**: Python 3.x
- **Web Framework**: Flask
- **Veri Kazıma**:
  - `requests`: HTTP istekleri için.
  - `BeautifulSoup4`: HTML parse etmek için.
  - `feedparser`: RSS akışlarını okumak için.
- **Doğal Dil İşleme (NLP)**:
  - `transformers`: Hugging Face modelleri için.
  - `openai`: GPT-4o-mini ve GPT-4 modellerine erişim.
- **Video ve Ses İşleme**:
  - `faster-whisper`: Yüksek performanslı ses-metin dönüştürme.
  - `moviepy`: Video klip oluşturma ve düzenleme.
  - `ffmpeg`: Ses ve video işlemleri.
- **Text-to-Speech (TTS)**:
  - `elevenlabs`: Metin seslendirme servisi.
- **Diğer**:
  - `python-dotenv`: Ortam değişkenlerini yönetmek için.
  - `numpy`: Video oluşturma işlemlerinde.
  - `Pillow`: Altyazı görselleri oluşturmak için.

### Frontend
- **3D Grafik**: three.js
- **Temel Teknolojiler**: HTML5, CSS3, JavaScript (ES6+)

---

## 🚀 Kurulum ve Çalıştırma

### Adım Adım Kurulum
1. **Projeyi Klonlayın**:
   ```bash
   git clone https://github.com/SevalSorak/Medya-Teknolojileri-Hackathonu.git
   cd Medya-Teknolojileri-Hackathonu
   ```

2. **Python Bağımlılıklarını Yükleyin**:
   ```bash
   pip install flask flask-cors requests beautifulsoup4 feedparser transformers torch torchvision torchaudio openai faster-whisper moviepy python-dotenv numpy Pillow elevenlabs
   ```
   *Not*: `torch` kurulumu sisteminize (CPU/GPU) göre değişiklik gösterebilir. Detaylar için [PyTorch web sitesini](https://pytorch.org/) ziyaret edin.

3. **API Anahtarlarını Yapılandırın**:
   - **OpenAI**: `backend/summarized_data.py` ve `backend/generate_video_shorts.py` dosyalarındaki `openai_api_key` değişkenine kendi OpenAI API anahtarınızı girin.
   - **ElevenLabs**: `backend` dizininde `.env` dosyası oluşturun ve içine şu şekilde anahtarlarınızı ekleyin:
     ```plaintext
     ELEVEN_API_KEY="YOUR_ELEVENLABS_API_KEY"
     VOICE_ID="YOUR_CHOSEN_VOICE_ID"
     ```

4. **Backend Servislerini Çalıştırın**:
   - **Veri Toplama (İsteğe Bağlı)**:
     ```bash
     python backend/aa_scraping.py
     python backend/rss_scraping.py
     ```
     Bu betikler `aa_cdx_verileri.json` ve `aa_haberler.csv` dosyalarını oluşturur/günceller.
   - **Veri Özetleme (İsteğe Bağlı)**:
     ```bash
     python backend/summarized_data.py
     ```
     Bu işlem, `data.json` dosyasını okur ve `summarized_data.json` dosyasını oluşturur.
   - **TTS Sunucusunu Başlatın**:
     ```bash
     python backend/voice.py
     ```
     Bu komut, `localhost:5000` üzerinde bir API sunucusu başlatır.

5. **Frontend’i Başlatın**:
   - En basit yöntem: `frontend/index.html` dosyasına çift tıklayarak tarayıcıda açın.
   - Daha stabil bir deneyim için yerel bir sunucu kullanın:
     ```bash
     npx http-server
     ```
   - Tarayıcıdan `http://localhost:8080` adresine gidin.

---
