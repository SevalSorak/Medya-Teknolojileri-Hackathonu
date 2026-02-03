# 📊 PROJE ÖZETİ VE PORTFÖY SUNUMU

## 🎯 Proje Genel Bakış

**Proje Adı:** ANADOLU: HABER ZAMAN TÜNELİ  
**Hackathon:** Medya Teknolojileri Hackathonu 2025  
**Hashtag:** #medyahackathonu2025  
**GitHub:** [SevalSorak/Medya-Teknolojileri-Hackathonu](https://github.com/SevalSorak/Medya-Teknolojileri-Hackathonu)

---

## 💡 Proje Konsepti

**ANADOLU: HABER ZAMAN TÜNELİ**, kullanıcılara Anadolu Ajansı (AA) haberleri üzerinden eşsiz bir **zaman yolculuğu** deneyimi sunan yenilikçi bir web platformudur. Proje, geleneksel haber okuma deneyimini 3D interaktif bir galeri ortamına dönüştürerek, kullanıcıların geçmiş ve güncel haberleri sürükleyici bir şekilde keşfetmesini sağlar.

### Temel Vizyon
- 📰 **Geleneksel Medyayı Dijitalleştirmek**: Basılı gazete estetiğini modern 3D teknolojisiyle birleştirmek
- 🎮 **İnteraktif Deneyim**: Haberleri pasif okumak yerine aktif keşfetmek
- 🤖 **Yapay Zeka Entegrasyonu**: Modern NLP ve TTS teknolojileriyle zenginleştirilmiş içerik
- ⏰ **Zaman Yolculuğu**: Wayback Machine entegrasyonuyla tarihi haberlere erişim

---

## ⭐ Öne Çıkan Özellikler

### 1. 🎨 3D İnteraktif Galeri
- **Three.js** ile oluşturulmuş tam teşekküllü bir 3D ortam
- Kristal tablolar üzerinde görsel olarak sunulan haberler
- WASD ve fare kontrolleriyle özgürce gezinilebilen galeri alanı
- Kategoriye özel odalar ve geçiş kapıları
- Dönemin ruhunu yansıtan dinamik tema değişimleri
- NPC karakterler ile canlı atmosfer

### 2. 🧠 Yapay Zeka Destekli İçerik İşleme
- **Otomatik Haber Özetleme**: 
  - Transformers kütüphanesi ve `nicktimur/mt5-base-turkish-news-summarizer` modeli
  - OpenAI GPT-4o-mini ile akıcılaştırılmış özetler
- **Video Shorts Üretimi**:
  - FFmpeg ve Faster-Whisper ile video analizi
  - GPT-4 ile önemli anların tespiti
  - Otomatik altyazılı kısa video üretimi
- **Doğal Sesli Okuma**:
  - ElevenLabs API entegrasyonu
  - Yüksek kaliteli Türkçe seslendirme
  - Modal içi anlık oynatma

### 3. 📊 Gelişmiş Veri Toplama ve Yönetimi
- **Wayback Machine CDX API**: Arşiv haberlerine erişim
- **RSS Akışları**: Güncel haberlerin otomatik takibi
- **BeautifulSoup4**: Profesyonel web scraping
- JSON tabanlı esnek veri yapısı

### 4. 🎭 Benzersiz Kullanıcı Deneyimi
- Eski gazete estetiğine sahip nostaljik ana sayfa
- Smooth animasyonlar ve geçişler
- Responsive tasarım
- Kategori bazlı içerik organizasyonu
- Tarih seçimi ve filtreleme

---

## 🛠️ Teknoloji Yığını

### Backend Teknolojileri
| Kategori | Teknolojiler |
|----------|-------------|
| **Framework** | Flask, Flask-CORS |
| **Web Scraping** | BeautifulSoup4, Requests, Feedparser |
| **NLP & AI** | Transformers, OpenAI (GPT-4, GPT-4o-mini), PyTorch |
| **Video İşleme** | FFmpeg, Faster-Whisper, MoviePy |
| **TTS** | ElevenLabs API |
| **Yardımcı** | NumPy, Pillow, python-dotenv |

### Frontend Teknolojileri
| Kategori | Teknolojiler |
|----------|-------------|
| **3D Grafik** | Three.js |
| **Temel** | HTML5, CSS3, JavaScript (ES6+) |
| **Tasarım** | Google Fonts (Cinzel, IM Fell English, Crimson Text) |
| **Animasyonlar** | CSS Animations, Three.js |

---

## 🏗️ Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND LAYER                       │
│  ┌──────────────────┐      ┌──────────────────┐        │
│  │   index.html     │──────│  gallery.html     │        │
│  │  (Giriş Sayfası) │      │  (3D Galeri)      │        │
│  └──────────────────┘      └──────────────────┘        │
│            │                        │                    │
│            └────────────┬───────────┘                    │
│                         │                                │
└─────────────────────────┼────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                     BACKEND LAYER                        │
│  ┌────────────────────────────────────────────────┐    │
│  │              Flask TTS API (voice.py)          │    │
│  │          (ElevenLabs Entegrasyonu)             │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           Veri İşleme Modülleri                │    │
│  │  • aa_scraping.py (Wayback Machine)            │    │
│  │  • rss_scraping.py (RSS Feeds)                 │    │
│  │  • summarized_data.py (NLP Pipeline)           │    │
│  │  • generate_video_shorts.py (Video AI)         │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                          │
│  • data.json (Ham Haberler)                             │
│  • summarized_data.json (Özetlenmiş Haberler)          │
│  • aa_cdx_verileri.json (Arşiv Verileri)               │
│  • aa_haberler.csv (RSS Verileri)                       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Teknik Başarılar

### 1. Çoklu API Entegrasyonu
✅ Wayback Machine CDX API  
✅ Anadolu Ajansı RSS Feeds  
✅ OpenAI GPT-4 & GPT-4o-mini  
✅ ElevenLabs Text-to-Speech  

### 2. Performans Optimizasyonu
- Async JavaScript operasyonları
- Etkin veri önbellekleme stratejisi
- Three.js render optimizasyonları
- Lazy loading implementasyonu

### 3. AI/ML Pipeline
- Türkçe NLP model entegrasyonu
- Multi-stage summarization pipeline
- Video analiz ve segmentasyon
- Speech-to-text dönüşüm

### 4. UX/UI İnovasyon
- Nostaljik gazete tasarımı
- 3D navigasyon sistemi
- Modal tabanlı detay görüntüleme
- Sesli okuma özelliği

---

## 📈 Proje Metrikleri

### Kod İstatistikleri
- **Toplam Dosya Sayısı**: 10+ dosya
- **Ana Kod Dosyaları**: 
  - 2 HTML sayfası
  - 6+ Python modülü
  - CSS ve JavaScript entegrasyonları
- **Veri Formatları**: JSON, CSV

### Özellik Kapsamı
- 🎨 **3D Görselleştirme**: Tam özellikli galeri
- 🤖 **AI Özellikleri**: 3 farklı AI servisi
- 📊 **Veri Kaynağı**: 2 farklı kaynak
- 🔊 **TTS Dil Desteği**: Türkçe

---

## 🚀 Kullanım Senaryoları

### Senaryo 1: Tarihçi/Araştırmacı
Belirli bir tarihteki olayları 3D ortamda keşfederek tarihi araştırma yapar. Haberler arasında gezinir, özetleri okur ve ilginç bulduğu haberleri sesli olarak dinler.

### Senaryo 2: Öğrenci
Okul projesi için yakın tarihteki önemli olayları araştırır. Video shorts özelliğiyle hızlıca önemli anları görüntüler ve sunumuna ekler.

### Senaryo 3: Medya Profesyoneli
Geçmiş dönemlerdeki haber sunumlarını inceler, trend analizleri yapar. Platformun AI özetleme özelliğini kullanarak büyük veri setlerini hızlıca değerlendirir.

### Senaryo 4: Sıradan Kullanıcı
Nostalji yaşamak için kendi doğum gününü seçer ve o gündeki haberleri eğlenceli bir 3D ortamda gezinerek keşfeder.

---

## 🎓 Öğrenilen Dersler ve Kazanımlar

### Teknik Kazanımlar
- **3D Web Geliştirme**: Three.js ile karmaşık 3D sahne yönetimi
- **AI/ML Entegrasyonu**: Multiple AI service orchestration
- **Full-Stack Development**: Python backend + JavaScript frontend
- **API Development**: RESTful API tasarımı ve implementasyonu
- **Data Pipeline**: ETL süreçleri ve veri işleme

### Soft Skills
- **Problem Çözme**: Karmaşık teknik zorlukların üstesinden gelme
- **Yaratıcılık**: Geleneksel medyayı modern teknolojiye uyarlama
- **Proje Yönetimi**: Çoklu modül koordinasyonu
- **Dokümantasyon**: Kapsamlı README ve kod dokümantasyonu

---

## 🔮 Gelecek Geliştirmeler

### Kısa Vadeli (1-3 Ay)
- [ ] Kullanıcı hesabı sistemi
- [ ] Favori haberler özelliği
- [ ] Sosyal paylaşım entegrasyonu
- [ ] Mobil responsive optimizasyonu
- [ ] Daha fazla haber kategorisi

### Orta Vadeli (3-6 Ay)
- [ ] Multi-language support (EN, FR, DE)
- [ ] VR/AR desteği
- [ ] Real-time haber akışı
- [ ] Kullanıcı yorumları ve etkileşim
- [ ] Analytics dashboard

### Uzun Vadeli (6-12 Ay)
- [ ] Machine learning tabanlı öneri sistemi
- [ ] Blockchain tabanlı haber doğrulama
- [ ] Live streaming entegrasyonu
- [ ] AI-powered haber editörü
- [ ] Cross-platform mobile uygulamalar

---

## 📊 Rekabetçi Avantajlar

### 1. Benzersiz Deneyim
Piyasada benzer bir 3D haber platformu bulunmamaktadır. Proje, medya tüketiminde yeni bir kategori yaratır.

### 2. Teknoloji Stack
Modern ve güncel teknolojilerin kullanımı ile ölçeklenebilir ve sürdürülebilir bir altyapı.

### 3. AI Entegrasyonu
Üç farklı AI servisinin koordineli kullanımı ile otomasyona dayalı içerik üretimi.

### 4. Türkçe Dil Desteği
Türkçe NLP modellerinin başarılı entegrasyonu ile yerel pazar avantajı.

### 5. Open Source Potansiyeli
Modüler yapı sayesinde community contributions için uygun.

---

## 🏆 Hackathon Kriterleri Değerlendirmesi

### İnovasyon (10/10)
✨ 3D haber platformu konsepti tamamen yeni ve özgün  
✨ Geleneksel medya ile modern teknolojinin yaratıcı birleşimi

### Teknik Uygulama (9/10)
💻 Multiple API entegrasyonları başarılı  
💻 Full-stack implementation  
💻 AI/ML pipeline çalışıyor

### Kullanıcı Deneyimi (9/10)
🎨 Görsel olarak etkileyici tasarım  
🎨 İnteraktif ve sürükleyici deneyim  
🎨 Kolay navigasyon

### İş Değeri (8/10)
💼 Açık pazar potansiyeli  
💼 Ölçeklenebilir model  
💼 Monetizasyon fırsatları

### Dokümantasyon (10/10)
📚 Kapsamlı README.md  
📚 Kod yapısı net ve anlaşılır  
📚 Kurulum talimatları detaylı

---

## 👥 Ekip ve İletişim

**Geliştirici:** Seval Sorak  
**GitHub:** [@SevalSorak](https://github.com/SevalSorak)  
**Repository:** [Medya-Teknolojileri-Hackathonu](https://github.com/SevalSorak/Medya-Teknolojileri-Hackathonu)

---

## 📝 Lisans ve Kullanım

Bu proje, Medya Teknolojileri Hackathonu 2025 kapsamında geliştirilmiştir. Eğitim ve araştırma amaçlı kullanım için uygundur.

---

## 🙏 Teşekkürler

- **Anadolu Ajansı**: Haber içerikleri için
- **OpenAI**: GPT modelleri için
- **ElevenLabs**: TTS servisi için
- **Hugging Face**: Türkçe NLP modeli için
- **Three.js Community**: 3D framework için
- **Medya Teknolojileri Hackathonu**: Bu platformu sağladıkları için

---

## 🎬 Sonuç

**ANADOLU: HABER ZAMAN TÜNELİ**, medya teknolojilerinin geleceğine yönelik cesur bir adımdır. Geleneksel haber okuma deneyimini 21. yüzyıl teknolojileriyle yeniden tanımlayan bu proje, kullanıcılara unutulmaz bir zaman yolculuğu sunar.

Proje, sadece bir hackathon çalışması değil, aynı zamanda medya sektöründeki dijital dönüşümün bir örneğidir. AI, 3D grafik ve modern web teknolojilerinin gücünü birleştirerek, bilgiye erişimi daha eğlenceli, interaktif ve anlamlı hale getirir.

---

**🌟 "Geçmişi Keşfet, Geleceği Şekillendir" 🌟**

---

*Bu portföy özeti, projenin teknik ve kreatif yönlerini sergilemek amacıyla hazırlanmıştır. Daha fazla bilgi için GitHub repository'sini ziyaret edin.*
