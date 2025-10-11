import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scraping_log.txt"),
        logging.StreamHandler()
    ]
)

# Retry mekanizması
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Kategoriler
categories = ["dunya", "gundem", "ekonomi", "haberler"]
cdx_url = "https://web.archive.org/cdx/search/cdx"

# Haber detay sayfasını parse et
def parse_news_page(archive_url, category, timestamp):
    try:
        response = session.get(archive_url, timeout=10)
        if response.status_code != 200:
            logging.error(f"Haber sayfası hatası: {archive_url} - Status {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Başlık
        title_elem = soup.select_one('h1.article-title, h2.news-heading, h3, a[itemprop="url"]')
        title = title_elem.text.strip() if title_elem else "Bulunamadı"
        if title == "Bulunamadı":
            logging.warning(f"{archive_url} için başlık bulunamadı")
        
        # İçerik
        content_div = soup.select_one('div#news-maincontent, div.article-post-content, div#haber, div.news-content, div.content')
        content = ""
        if content_div:
            p_elements = content_div.select('p.selectionShareable, p') or content_div.find_all('p')
            for p in p_elements:
                content += p.text.strip() + "\n"
            h3_elements = content_div.select('h3') or content_div.find_all('h3')
            for h3 in h3_elements:
                content += h3.text.strip() + "\n"
        else:
            logging.warning(f"{archive_url} için içerik bulunamadı")
        
        # Tarih
        date_elem = soup.select_one('meta[name="date"], span.fa.fa-calendar, span.date, div.publish-date, time, div.kunye span')
        date = date_elem.get('content') or date_elem.text.strip() if date_elem else timestamp[:8]
        
        # Kategori
        category_elem = soup.select_one(f'a[title="{category}"], a[href*="/tr/{category}"], span.fa.fa-categories a, span.category')
        parsed_category = category_elem.text.strip() if category_elem else category if category else "Bilinmiyor"
        
        # Görsel
        image_elem = soup.select_one('img.open-popup.img-responsive, .news-image, img')
        image_url = image_elem['src'] if image_elem and image_elem.get('src') else "Bulunamadı"
        
        # Özet
        summary_elem = soup.select('p.selectionShareable, p')[0] if soup.select('p.selectionShareable, p') else None
        summary = summary_elem.text.strip() if summary_elem else content[:200].strip() if content else "Bulunamadı"
        
        article_data = {
            "archive_url": archive_url,
            "title": title,
            "content": content.strip(),
            "date": date,
            "category": parsed_category,
            "image_url": image_url,
            "summary": summary
        }
        logging.info(f"İşlenen: {title} ({date}) - Kategori: {parsed_category} - İçerik uzunluğu: {len(content)} karakter")
        return article_data
    except Exception as e:
        logging.error(f"Haber parse hatası: {archive_url} - {str(e)}")
        return None

# Liste sayfasından haber linklerini çek
def get_news_links(archive_url, category):
    try:
        response = session.get(archive_url, timeout=10)
        if response.status_code != 200:
            logging.error(f"Liste sayfası hatası: {archive_url} - Status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        news_links = []
        for link_elem in soup.select('h3 a[href*="tr/haberler"], h3 a[href*="tr/dunya"], h3 a[href*="tr/gundem"], h3 a[href*="tr/ekonomi"]'):
            href = link_elem.get('href')
            if href.startswith('/web/'):
                full_url = f"https://web.archive.org{href}"
            elif href.startswith('http'):
                full_url = href
            else:
                full_url = f"https://web.archive.org/web/{archive_url.split('/web/')[1].split('/')[0]}/{href}"
            news_links.append(full_url)
        logging.info(f"{archive_url} için {len(news_links)} haber linki bulundu")
        return news_links
    except Exception as e:
        logging.error(f"Liste parse hatası: {archive_url} - {str(e)}")
        return []

# Fallback Availability API
def get_alternative_snapshot(original_url):
    try:
        response = session.get("http://archive.org/wayback/available", params={"url": original_url}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["archived_snapshots"].get("closest"):
                return data["archived_snapshots"]["closest"]["url"]
        return None
    except Exception as e:
        logging.error(f"Availability API hatası: {original_url} - {str(e)}")
        return None

# CDX sorgusu
articles = []
for category in categories:
    params = {
        "url": f"aa.com.tr/tr/{category}/*",
        "matchType": "prefix",
        "from": "20100101",
        "to": "20250928",
        "output": "json",
        "limit": 100,
        "gzip": "false"
    }
    
    try:
        # Sayfalama için toplam sayfa sayısı
        params["showNumPages"] = "true"
        response = session.get(cdx_url, params=params, timeout=10)
        num_pages = int(response.text) if response.status_code == 200 and response.text.strip().isdigit() else 1
        logging.info(f"Kategori {category}: {num_pages} sayfa bulundu")
        params.pop("showNumPages")
        
        for page in range(min(num_pages, 10)):
            params["page"] = page
            logging.info(f"CDX sorgusu: {cdx_url} - Kategori: {category} - Sayfa: {page} - Parametreler: {params}")
            response = session.get(cdx_url, params=params, timeout=10)
            logging.info(f"CDX Status: {response.status_code}")
            logging.info(f"CDX Yanıt Metni (ilk 500 karakter): {response.text[:500]}")
            
            if response.status_code != 200:
                logging.error(f"CDX hatası: Status {response.status_code}")
                continue
            
            try:
                data = response.json()
                logging.info(f"CDX JSON uzunluğu: {len(data)}")
                logging.info(f"CDX JSON ilk satır: {data[0] if data else 'Boş'}")
            except json.JSONDecodeError as je:
                logging.error(f"JSON parse hatası: {je} - Yanıt: {response.text}")
                continue
            
            snapshots = data[1:] if len(data) > 1 else []
            logging.info(f"Kategori {category}, Sayfa {page}: {len(snapshots)} snapshot alındı")
            
            if not snapshots and category == "haberler" and page == 0:
                logging.warning(f"{category} için snapshot yok - Genel sorgu dene")
                params["url"] = "aa.com.tr/*"
                response = session.get(cdx_url, params=params, timeout=10)
                logging.info(f"Yeni CDX Yanıt Metni (ilk 500): {response.text[:500]}")
                try:
                    data = response.json()
                    snapshots = data[1:] if len(data) > 1 else []
                    logging.info(f"Yeni toplam {len(snapshots)} snapshot alındı")
                except json.JSONDecodeError as je:
                    logging.error(f"Yeni JSON parse hatası: {je} - Yanıt: {response.text}")
                    continue
            
            for snap in snapshots:
                timestamp, original = snap[1], snap[2]
                archive_url = f"https://web.archive.org/web/{timestamp}/{original}"
                logging.info(f"Snapshot işleniyor: {archive_url}")
                
                # Liste sayfası kontrolü
                if "/tr/haberler" in original or "/*" in original:
                    news_links = get_news_links(archive_url, category)
                    for news_url in news_links:
                        article_data = parse_news_page(news_url, category, timestamp)
                        if article_data is None:
                            alt_url = get_alternative_snapshot(news_url.split('/web/')[1].split('/', 1)[1])
                            if alt_url:
                                logging.info(f"Alternatif snapshot denleniyor: {alt_url}")
                                article_data = parse_news_page(alt_url, category, timestamp)
                        if article_data:
                            articles.append(article_data)
                        time.sleep(2)
                else:
                    article_data = parse_news_page(archive_url, category, timestamp)
                    if article_data is None:
                        alt_url = get_alternative_snapshot(original)
                        if alt_url:
                            logging.info(f"Alternatif snapshot denleniyor: {alt_url}")
                            article_data = parse_news_page(alt_url, category, timestamp)
                    if article_data:
                        articles.append(article_data)
                
                time.sleep(2)  # Rate limit
    except Exception as e:
        logging.error(f"Kategori {category} genel hatası: {str(e)}")

# Verileri kaydet
if articles:
    with open("aa_cdx_verileri.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    logging.info(f"Toplam {len(articles)} haber kaydedildi")
else:
    logging.warning("Hiç veri çekilemedi - Logları kontrol et")