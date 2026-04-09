from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import requests
import re
import os

app = FastAPI()

BASE = "https://cinverse.name.ng"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED ACCESS - SILENT TECH 🖕")

# --- SERVE THE UI AT ROOT ---
@app.get("/", response_class=HTMLResponse)
def read_root():
    # This reads your professional UI file and serves it at the main link
    try:
        with open("public/index.html", "r") as f:
            return f.read()
    except:
        # Fallback if file isn't found during build
        return "<h1>SILENT TECH UI LOADING...</h1><p>If you see this, check your folder structure.</p>"

# --- API ENDPOINTS ---

@app.get("/api/v1/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/v1/search")
def search(q: str, key: str = "silent"):
    validate(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}

@app.get("/api/v1/movie")
def movie(slug: str, key: str = "silent"):
    validate(key)
    p = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    num_id = re.search(r'"id":"(\d{15,20})"', p.text)
    if not num_id: return {"error": "Movie not found"}
    src = requests.get(f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}", headers=HEADERS).json()
    return {"provider": "SILENT TECH", "slug": slug, "id": num_id.group(1), "media": src}

@app.get("/api/v1/categories")
def cats(key: str = "silent"):
    validate(key)
    return {
        "provider": "SILENT TECH",
        "list": ["Trending", "Action", "Adventure", "Animation", "Comedy", "Crime", "Horror", "Sci-Fi", "Drama"]
    }
