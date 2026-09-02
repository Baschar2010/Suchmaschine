from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def search_real_web(query):
    if not query:
        return []
    
    results = []
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for result in soup.find_all("div", class_="result"):
                title_elem = result.find("a", class_="result__url")
                snippet_elem = result.find("a", class_="result__snippet")
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get("href", "#")
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    results.append({
                        "title": title,
                        "display_url": link,
                        "url": link,
                        "snippet": snippet
                    })
    except Exception as e:
        print(f"Error fetching search results: {e}")
        
    return results

AL_AQSA_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% if query %}Al-Aqsa Suche: {{ query }}{% else %}Al-Aqsa Suche{% endif %}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #fff;
            color: #202124;
        }
        .home-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .home-logo-icon {
            font-size: 64px;
            margin-bottom: 10px;
        }
        .home-logo-text {
            font-size: 48px;
            font-weight: bold;
            color: #1a73e8;
            margin-bottom: 20px;
        }
        .home-search-box, .header-search-form {
            display: flex;
            width: 100%;
            max-width: 600px;
            border: 1px solid #dfe1e5;
            border-radius: 24px;
            padding: 8px 16px;
            box-shadow: none;
            background: #fff;
        }
        .home-search-box:hover, .header-search-form:hover {
            box-shadow: 0 1px 6px rgba(32,33,36,.28);
        }
        .home-search-box input, .header-search-form input {
            flex: 1;
            border: none;
            outline: none;
            font-size: 16px;
        }
        .home-search-box button, .header-search-form button {
            background-color: #1a73e8;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .header {
            display: flex;
            align-items: center;
            padding: 12px 24px;
            border-bottom: 1px solid #dfe1e5;
        }
        .header-brand {
            font-size: 20px;
            font-weight: bold;
            color: #1a73e8;
            text-decoration: none;
            margin-right: 20px;
        }
        .main-layout {
            padding: 20px 24px;
        }
        .stats {
            font-size: 14px;
            color: #70757a;
            margin-bottom: 20px;
        }
        .result-card {
            margin-bottom: 24px;
            max-width: 650px;
        }
        .result-url {
            font-size: 12px;
            color: #202124;
        }
        .result-title {
            font-size: 16px;
            color: #1a0dab;
            text-decoration: none;
            display: block;
            margin-top: 2px;
            margin-bottom: 3px;
        }
        .result-title:hover {
            text-decoration: underline;
        }
        .result-snippet {
            font-size: 14px;
            color: #4d5156;
        }
    </style>
</head>
<body>

    {% if not query %}
    <div class="home-container">
        <div class="home-logo-icon">🕌</div>
        <div class="home-logo-text">Al-Aqsa Suche</div>
        <form method="GET" action="" class="home-search-box">
            <input type="text" name="q" placeholder="Suchbegriff eingeben..." autocomplete="off" autofocus required>
            <button type="submit">Suchen</button>
        </form>
    </div>
    {% else %}
    <div class="header">
        <a href="/" class="header-brand">🕌 Al-Aqsa</a>
        <form method="GET" action="" class="header-search-form">
            <input type="text" name="q" value="{{ query }}" autocomplete="off" required>
            <button type="submit">Suche</button>
        </form>
    </div>
    <div class="main-layout">
        <div class="stats">Ungefähr {{ results|length * 340000 }} Ergebnisse (0,15 Sekunden)</div>
        {% for item in results %}
        <div class="result-card">
            <div class="result-url">{{ item.display_url }}</div>
            <a href="{{ item.url }}" target="_blank" rel="noopener noreferrer" class="result-title">{{ item.title }}</a>
            <div class="result-snippet">{{ item.snippet }}</div>
        </div>
        {% endfor %}
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