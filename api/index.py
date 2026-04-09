from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import requests
import re
import json

app = FastAPI()

# --- THE ENGINE ---
BASE = "https://cinverse.name.ng"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- THE FRONTEND (Embedded Glassmorphism Pro Dashboard) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT API | PRO DASHBOARD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #050506; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .card { background: #0f1115; border: 1px solid #1f2937; border-radius: 1.5rem; transition: all 0.3s ease; }
        .card:hover { border-color: #3b82f6; transform: translateY(-2px); }
        .input-field { background: #08090b; border: 1px solid #2d3748; border-radius: 12px; padding: 12px; color: #fff; width: 100%; outline: none; }
        .input-field:focus { border-color: #3b82f6; box-shadow: 0 0 10px rgba(59, 130, 246, 0.2); }
        .response-box { background: #000; border: 1px solid #2d3748; border-radius: 15px; padding: 20px; font-family: 'Courier New', monospace; font-size: 11px; color: #60a5fa; overflow-x: auto; min-height: 300px; }
        .ios-dot { width: 11px; height: 11px; border-radius: 50%; }
    </style>
</head>
<body class="p-6 md:p-10">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER -->
        <nav class="glass rounded-[30px] p-6 flex justify-between items-center mb-10">
            <div class="flex items-center gap-6">
                <div class="flex gap-1.5">
                    <div class="ios-dot bg-[#ff5f57]"></div><div class="ios-dot bg-[#ffbd2e]"></div><div class="ios-dot bg-[#28c840]"></div>
                </div>
                <h1 class="text-2xl font-black tracking-tighter">SILENT <span class="text-blue-500 text-[10px] tracking-[6px] ml-2">API PLATFORM</span></h1>
            </div>
            <div class="hidden md:block text-[9px] font-bold opacity-30 tracking-[4px]">SILENT TECH ECOSYSTEM v2.0</div>
        </nav>

        <!-- STATS CARDS -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            <div class="glass p-8 rounded-3xl text-center"><div class="text-blue-500 text-3xl font-black mb-1">8</div><div class="text-[9px] opacity-40 font-bold uppercase tracking-[2px]">Core Endpoints</div></div>
            <div class="glass p-8 rounded-3xl text-center"><div class="text-emerald-500 text-3xl font-black mb-1">100%</div><div class="text-[9px] opacity-40 font-bold uppercase tracking-[2px]">Uptime Status</div></div>
            <div class="glass p-8 rounded-3xl text-center"><div class="text-purple-500 text-3xl font-black mb-1">GET</div><div class="text-[9px] opacity-40 font-bold uppercase tracking-[2px]">JSON Methods</div></div>
            <div class="glass p-8 rounded-3xl text-center"><div class="text-orange-500 text-3xl font-black mb-1">∞</div><div class="text-[9px] opacity-40 font-bold uppercase tracking-[2px]">Rate Limit</div></div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <!-- ENDPOINT LIST -->
            <div class="lg:col-span-4 space-y-4">
                <h2 class="text-xs font-black opacity-30 tracking-[5px] mb-6">ENDPOINT SELECTION</h2>
                <div onclick="setEndpoint('search')" class="card p-5 cursor-pointer flex items-center gap-4">
                    <div class="bg-blue-500/10 p-3 rounded-xl text-blue-500"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg></div>
                    <div><div class="font-bold text-sm">Search Movies</div><div class="text-[10px] opacity-40">/api/search</div></div>
                </div>
                <div onclick="setEndpoint('media')" class="card p-5 cursor-pointer flex items-center gap-4">
                    <div class="bg-emerald-500/10 p-3 rounded-xl text-emerald-500"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg></div>
                    <div><div class="font-bold text-sm">Stream & Links</div><div class="text-[10px] opacity-40">/api/media</div></div>
                </div>
                <div onclick="setEndpoint('trending')" class="card p-5 cursor-pointer flex items-center gap-4">
                    <div class="bg-orange-500/10 p-3 rounded-xl text-orange-500"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg></div>
                    <div><div class="font-bold text-sm">Trending Content</div><div class="text-[10px] opacity-40">/api/trending</div></div>
                </div>
            </div>

            <!-- INTERACTIVE TESTER -->
            <div class="lg:col-span-8">
                <div class="glass rounded-[35px] p-8">
                    <div class="flex justify-between items-center mb-8">
                        <h3 id="test-title" class="text-xl font-bold">Interactive Playground</h3>
                        <span id="method-tag" class="bg-blue-600 px-3 py-1 rounded-full text-[9px] font-black uppercase">GET</span>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <div>
                            <label class="text-[10px] font-bold opacity-30 mb-2 block uppercase">API Key</label>
                            <input id="key-in" class="input-field" value="silent">
                        </div>
                        <div>
                            <label id="param-label" class="text-[10px] font-bold opacity-30 mb-2 block uppercase">Parameter</label>
                            <input id="param-in" class="input-field" value="Spider-Man">
                        </div>
                    </div>

                    <button onclick="executeTest()" class="w-full bg-blue-600 hover:bg-blue-500 py-4 rounded-2xl font-bold transition-all active:scale-95 mb-8">SEND REQUEST</button>

                    <div class="response-box relative">
                        <div class="absolute top-4 right-4 text-[9px] opacity-30 font-bold uppercase tracking-[2px]">JSON Output</div>
                        <pre id="json-view">Waiting for execution...</pre>
                    </div>
                </div>
            </div>
        </div>

        <footer class="mt-20 text-center pb-20">
            <div class="h-[1px] bg-white/5 w-full mb-10"></div>
            <p class="text-[9px] tracking-[15px] opacity-20 font-black uppercase">ALL RIGHTS RESERVED TO SILENT TECH | MADE WITH MIDDLE FINGER 🖕</p>
        </footer>
    </div>

    <script>
        let currentMode = 'search';
        function setEndpoint(mode) {
            currentMode = mode;
            document.getElementById('test-title').innerText = "Testing: " + mode.toUpperCase();
            if(mode === 'search') {
                document.getElementById('param-label').innerText = "Query";
                document.getElementById('param-in').value = "Spider-Man";
            } else if(mode === 'media') {
                document.getElementById('param-label').innerText = "Movie Slug";
                document.getElementById('param-in').value = "spider-man-homecoming-ylSxcJY0uNa";
            } else {
                document.getElementById('param-label').innerText = "Type";
                document.getElementById('param-in').value = "ALL";
            }
        }

        async function executeTest() {
            const out = document.getElementById('json-view');
            const key = document.getElementById('key-in').value;
            const param = document.getElementById('param-in').value;
            out.innerText = "Requesting Silent Tech Cluster...";

            let url = "";
            if(currentMode === 'search') url = `/api/search?q=${param}&key=${key}`;
            if(currentMode === 'media') url = `/api/media?slug=${param}&key=${key}`;
            if(currentMode === 'trending') url = `/api/trending?key=${key}`;

            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "CRITICAL SERVER ERROR."; }
        }
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC ---

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_UI

@app.get("/api/search")
def search(q: str = "Spider", key: str = "silent"):
    validate(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}

@app.get("/api/media")
def media(slug: str, key: str = "silent"):
    validate(key)
    p = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    num_id = re.search(r'"id":"(\d{15,20})"', p.text)
    if not num_id: return {"error": "Media not found"}
    src = requests.get(f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}", headers=HEADERS).json()
    return {"provider": "SILENT TECH", "media": src}

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/categories")
def cats(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "categories": ["Action", "Adventure", "Horror", "Comedy", "Sci-Fi", "Crime"]}

@app.get("/api/homepage")
def home_data(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "status": "Home data synced"}
