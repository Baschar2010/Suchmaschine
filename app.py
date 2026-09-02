import logging
import urllib.parse
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template_string, request

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

def search_real_web(query):
    if not query:
        return []
    
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    data = {"q": query}
    
    results = []
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for result in soup.select(".result"):
            title_elem = result.select_one(".result__title")
            snippet_elem = result.select_one(".result__snippet")
            url_elem = result.select_one(".result__url")
            
            if title_elem and url_elem:
                title = title_elem.get_text(strip=True)
                display_url = url_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                
                # Echten Ziel-Link aus DuckDuckGo extrahieren
                a_tag = title_elem.find("a")
                real_url = display_url
                if a_tag and "href" in a_tag:
                    raw_href = a_tag["href"]
                    if "uddg=" in raw_href:
                        parsed_url = urllib.parse.urlparse(raw_href)
                        qs = urllib.parse.parse_qs(parsed_url.query)
                        if "uddg" in qs:
                            real_url = qs["uddg"][0]
                
                # Sicherstellen, dass die URL mit http:// oder https:// beginnt
                if not real_url.startswith("http://") and not real_url.startswith("https://"):
                    real_url = "https://" + real_url

                results.append({
                    "title": title,
                    "url": real_url,
                    "display_url": display_url,
                    "snippet": snippet
                })
    except Exception as e:
        logging.error(f"Fehler beim Web-Scraping: {e}")
        
    if not results:
        results.append({
            "title": f"Ergebnisse für {query}",
            "url": f"https://www.google.com/search?q={query}",
            "display_url": "www.google.com",
            "snippet": "Keine direkten Live-Treffer gefunden."
        })
        
    return results

AL_AQSA_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ query + ' - Al-Aqsa Suche' if query else 'Al-Aqsa Suchmaschine' }}</title>
<style>
body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #fff; color: #202124; }
.home-container { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 85vh; padding-top: 40px; }
.home-logo-box { display: flex; flex-direction: column; align-items: center; margin-bottom: 25px; }
.home-logo-icon { width: 110px; height: 110px; background: #e8f0fe; color: #1a73e8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 55px; border: 3px solid #1a73e8; margin-bottom: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
.home-logo-text { font-size: 45px; font-weight: bold; color: #1a73e8; letter-spacing: -1px; }
.home-search-box { display: flex; width: 580px; max-width: 90%; border: 1px solid #dfe1e5; border-radius: 24px; padding: 10px 16px; align-items: center; box-shadow: 0 1px 6px rgba(32,33,36,0.1); margin-bottom: 30px; background: #fff; }
.home-search-box input { flex: 1; border: none; outline: none; font-size: 16px; background: transparent; margin-left: 10px; }
.home-search-box button { background: #1a73e8; color: white; border: none; padding: 8px 18px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.header { display: flex; align-items: center; padding: 12px 24px; border-bottom: 1px solid #dfe1e5; position: sticky; top: 0; background: white; z-index: 100; }
.header-brand { display: flex; align-items: center; text-decoration: none; margin-right: 30px; gap: 12px; }
.header-logo-icon { width: 40px; height: 40px; background: #e8f0fe; color: #1a73e8; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; border: 2px solid #1a73e8; }
.header-logo-text { font-size: 20px; font-weight: bold; color: #1a73e8; }
.header-search-form { display: flex; width: 650px; border: 1px solid #dfe1e5; border-radius: 24px; padding: 6px 16px; align-items: center; box-shadow: 0 1px 6px rgba(32,33,36,0.05); background: #fff; }
.header-search-form input { flex: 1; border: none; outline: none; font-size: 16px; background: transparent; }
.header-search-form button { background: #1a73e8; color: white; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.main-layout { display: flex; padding: 20px 200px; max-width: 1250px; }
.results-column { flex: 1; max-width: 680px; }
.stats { color: #70757a; font-size: 13px; margin-bottom: 15px; }
.result-card { margin-bottom: 26px; }
.result-url { font-size: 12px; color: #006621; word-break: break-all; margin-bottom: 2px; }
.result-title { font-size: 20px; color: #1a0dab; text-decoration: none; display: inline-block; margin-bottom: 3px; }
.result-title:hover { text-decoration: underline; }
.result-snippet { font-size: 14px; color: #4d5156; line-height: 1.5; }
</style>
</head>
<body>
{% if not query %}
<div class="home-container">
    <div class="home-logo-box">
        <div class="home-logo-icon">🕌</div>
        <div class="home-logo-text">Al-Aqsa Suche</div>
    </div>
    <form method="GET" action="/" class="home-search-box">
        <input type="text" name="q" placeholder="Suchbegriff eingeben..." autocomplete="off" autofocus required>
        <button type="submit">Suchen</button>
    </form>
</div>
{% else %}
<div class="header">
    <a href="/" class="header-brand">
        <div class="header-logo-icon">🕌</div>
        <span class="header-logo-text">Al-Aqsa</span>
    </a>
    <form method="GET" action="/" class="header-search-form">
        <input type="text" name="q" value="{{ query }}" autocomplete="off" required>
        <button type="submit">Suche</button>
    </form>
</div>
<div class="main-layout">
    <div class="results-column">
        <div class="stats">Ungefähr {{ results|length * 340000 }} Ergebnisse (0,15 Sekunden)</div>
        {% for item in results %}
            <div class="result-card">
                <div class="result-url">{{ item.display_url }}</div>
                <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer" class="result-title">{{ item.title }}</a>
                <div class="result-snippet">{{ item.snippet }}</div>
            </div>
        {% endfor %}
    </div>
</div>
{% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    results = search_real_web(query)
    return render_template_string(AL_AQSA_TEMPLATE, query=query, results=results)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)