import feedparser
import csv

# Çekmek istediğin kategoriler
categories = ["guncel", "ekonomi", "spor", "dunya", "teknoloji", "politika", "kultur-sanat", "yasam", "saglik"]

all_entries = []

for cat in categories:
    url = f"https://www.aa.com.tr/tr/rss/default?cat={cat}"
    feed = feedparser.parse(url)
    print(f"{cat.upper()} kategorisinde {len(feed.entries)} haber bulundu.")
    
    for entry in feed.entries:
        all_entries.append({
            "kategori": cat,
            "baslik": entry.title,
            "link": entry.link,
            "tarih": entry.published,
            "ozet": entry.summary
        })

print("\nToplam çekilen haber sayısı:", len(all_entries))

# Verileri CSV dosyasına kaydetme
if all_entries:
    csv_file_name = "aa_haberler.csv"
    # Sütun başlıklarını all_entries listesindeki ilk elemanın anahtarlarından alıyoruz
    fieldnames = all_entries[0].keys()

    try:
        with open(csv_file_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_entries)
        print(f"Veriler başarıyla '{csv_file_name}' dosyasına kaydedildi.")
    except IOError:
        print(f"Hata: '{csv_file_name}' dosyasına yazılamadı.")
