from fastapi import FastAPI, HTTPException, Query
import requests
import re

app = FastAPI()

BASE = "https://cinverse.name.ng"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def validate_key(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="UNAUTHORIZED BY SILENT TECH 🖕")

@app.get("/api/v1/search")
def search(q: str, key: str = "silent"):
    validate_key(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}

@app.get("/api/v1/movie")
def movie(slug: str, key: str = "silent"):
    validate_key(key)
    p = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    num_id = re.search(r'"id":"(\d{15,20})"', p.text)
    if not num_id: return {"error": "Movie not found"}
    src = requests.get(f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}", headers=HEADERS).json()
    return {"provider": "SILENT TECH", "slug": slug, "id": num_id.group(1), "media": src}

@app.get("/api/v1/trending")
def trending(key: str = "silent"):
    validate_key(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "list": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:10]]}

@app.get("/api/v1/categories")
def cats(key: str = "silent"):
    validate_key(key)
    return {"provider": "SILENT TECH", "categories": ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Horror", "Sci-Fi"]}
