import urllib.parse
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
}

def fetch_social_and_web_mentions(keyword: str, time_range: str = "all") -> List[Dict[str, Any]]:
    """
    Mengambil konten, postingan akun, video, dan perbincangan publik dari berbagai
    platform media sosial (TikTok, Instagram, X/Twitter, YouTube, LinkedIn, Media Berita)
    dengan dukungan filter rentang waktu.
    """
    time_filter = ""
    if time_range == "24h":
        time_filter = " when:1d"
    elif time_range == "7d":
        time_filter = " when:7d"
    elif time_range == "30d":
        time_filter = " when:30d"

    platforms = [
        ("TikTok", f"site:tiktok.com {keyword}{time_filter}", 8),
        ("Instagram", f"site:instagram.com {keyword}{time_filter}", 8),
        ("X (Twitter)", f"(site:twitter.com OR site:x.com) {keyword}{time_filter}", 6),
        ("YouTube", f"site:youtube.com {keyword}{time_filter}", 6),
        ("LinkedIn", f"site:linkedin.com {keyword}{time_filter}", 5),
        ("Media Online", f"{keyword}{time_filter}", 10)
    ]
    
    all_items = []
    seen_titles = set()
    
    for channel_name, query, limit in platforms:
        try:
            enc = urllib.parse.quote(query)
            rss_url = f"https://news.google.com/rss/search?q={enc}&hl=id&gl=ID&ceid=ID:id"
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:limit]:
                title = entry.get("title", "")
                summary_html = entry.get("summary", "")
                soup = BeautifulSoup(summary_html, "html.parser")
                summary_text = soup.get_text()
                link = entry.get("link", "#")
                pub_date = entry.get("published", "")
                
                clean_title = title
                for suffix in [
                    " - TikTok", " - tiktok.com", " - instagram.com", " - Instagram",
                    " - X", " - Twitter", " - YouTube", " - Kompas.com", " - Detikcom",
                    " - Tempo.co", " - LinkedIn"
                ]:
                    if clean_title.endswith(suffix):
                        clean_title = clean_title[:-len(suffix)]
                
                if clean_title and clean_title not in seen_titles:
                    seen_titles.add(clean_title)
                    all_items.append({
                        "source": f"{channel_name}",
                        "channel": channel_name,
                        "title": clean_title,
                        "content": summary_text if summary_text else f"Aktivitas dan ulasan publik seputar {keyword} di platform {channel_name}.",
                        "author": f"{channel_name} Creator / User",
                        "date": pub_date or datetime.now().strftime("%d %b %Y"),
                        "url": link
                    })
        except Exception as e:
            print(f"[Warn Scraper {channel_name}] {e}")
            
    return all_items

def build_social_deep_links(keyword: str) -> List[Dict[str, Any]]:
    """
    Menyediakan link eksplorasi sosial media dan e-commerce terarah
    agar pengguna bisa langsung membuka pencarian live di platform masing-masing.
    """
    enc = urllib.parse.quote(keyword)
    return [
        {
            "source": "TikTok Live",
            "channel": "TikTok",
            "title": f"Buka tren video & komentar '{keyword}' di TikTok",
            "content": f"Eksplorasi langsung video FYP, ulasan konten kreator, dan tagar #{keyword} di aplikasi TikTok.",
            "author": "TikTok Search",
            "date": datetime.now().strftime("%d %b %Y"),
            "url": f"https://www.tiktok.com/search?q={enc}"
        },
        {
            "source": "Instagram Live",
            "channel": "Instagram",
            "title": f"Cari postingan, reels & tagar '{keyword}' di Instagram",
            "content": f"Lihat postingan feeds, testimoni reels, dan akun resmi terkait '{keyword}' di Instagram.",
            "author": "Instagram Search",
            "date": datetime.now().strftime("%d %b %Y"),
            "url": f"https://www.instagram.com/explore/tags/{enc}/"
        },
        {
            "source": "X (Twitter) Live",
            "channel": "X (Twitter)",
            "title": f"Pantau percakapan warganet tentang '{keyword}' di X (Twitter)",
            "content": f"Temukan mention, keluhan, dan pujian real-time dari warganet Twitter/X seputar '{keyword}'.",
            "author": "X Search",
            "date": datetime.now().strftime("%d %b %Y"),
            "url": f"https://x.com/search?q={enc}&f=live"
        },
        {
            "source": "Tokopedia",
            "channel": "E-Commerce",
            "title": f"Ulasan pembeli terverifikasi '{keyword}' di Tokopedia",
            "content": f"Lihat ribuan ulasan kepuasan produk, rating bintang, dan feedback konsumen nyata untuk '{keyword}'.",
            "author": "Tokopedia Search",
            "date": datetime.now().strftime("%d %b %Y"),
            "url": f"https://www.tokopedia.com/search?st=product&q={enc}"
        }
    ]

def fetch_all_trend_data(keyword: str, time_range: str = "all") -> List[Dict[str, Any]]:
    """
    Mengambil data riil dari seluruh platform media sosial & berita
    secara terarah dan akurat dengan filter waktu.
    """
    social_items = fetch_social_and_web_mentions(keyword, time_range=time_range)
    deep_links = build_social_deep_links(keyword)
    
    combined = social_items + deep_links
    print(f"[Scraper] '{keyword}' ({time_range}): Ditemukan {len(social_items)} percakapan multi-platform + {len(deep_links)} direct search links.")
    return combined
