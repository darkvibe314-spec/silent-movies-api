from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import re
import json
import base64
from urllib.parse import unquote

app = FastAPI()

# --- CONFIG ---
BASE = "https://cinverse.name.ng"
# Session with persistence to keep the site from blocking us
session = requests.Session()
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
    "referer": BASE
}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- GHOST PROXY SYSTEM ---
def create_ghost_link(original_url: str, request: Request):
    try:
        encoded = base64.b64encode(original_url.encode()).decode()
        base_api_url = str(request.base_url).rstrip('/')
        return f"{base_api_url}/api/v1/ghost?data={encoded}"
    except: return original_url

@app.get("/api/v1/ghost")
def ghost_proxy(data: str):
    try:
        real_url = base64.b64decode(data).decode()
        # Direct redirect allows browser headers to take over
        return RedirectResponse(url=real_url)
    except:
        return {"error": "GHOST_LINK_BROKEN"}

# --- THE PREMIUM 3D UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT TECH | GHOST v14</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #020204; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; perspective: 1200px; overflow-x: hidden; }
        .glass-3d { 
            background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(40px); 
            border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: 0 25px 50px rgba(0,0,0,0.8);
            transform-style: preserve-3d; transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        }
        .card-3d:hover { transform: translateZ(40px) rotateX(2deg) rotateY(-2deg); border-color: #3b82f6; background: rgba(59, 130, 246, 0.05); }
        .card-3d:active { transform: scale(0.96); }
        .response-box { 
            background: #000; border: 1px solid #1f2937; border-radius: 25px; padding: 25px; 
            font-family: 'Courier New', monospace; font-size: 11px; color: #60a5fa; 
            overflow: auto; max-height: 550px; white-space: pre-wrap; word-break: break-all;
        }
        .doc-section { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 35px; padding: 35px; margin-bottom: 30px; }
        .ios-dot { width: 12px; height: 12px; border-radius: 50%; }
        ::-webkit-scrollbar { width: 4px; } ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
        .transmit-btn { 
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
        }
    </style>
</head>
<body class="p-4 md:p-12 lg:p-24">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER -->
        <header class="glass-3d rounded-[50px] p-10 flex justify-between items-center mb-16">
            <div class="flex items-center gap-6">
                <div class="flex gap-2"><div class="ios-dot bg-[#ff5f57]"></div><div class="ios-dot bg-[#ffbd2e]"></div><div class="ios-dot bg-[#28c840]"></div></div>
                <h1 class="text-3xl font-black tracking-tighter uppercase italic">Silent <span class="text-blue-500 not-italic">Ghost</span></h1>
            </div>
            <div class="hidden md:block text-[10px] font-black opacity-30 tracking-[10px] uppercase">Proxy_Node_v14_GodMode</div>
        </header>

        <!-- DASHBOARD GRID -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            <div onclick="setE('/api/search', 'Spider-Man')" class="glass-3d card-3d p-8 rounded-[35px]">
                <p class="text-[11px] font-black text-blue-500 mb-2 tracking-widest">01. SEARCH</p>
                <p class="text-xs opacity-40 uppercase">JSON Crawler</p>
            </div>
            <div onclick="setE('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d p-8 rounded-[35px] border-blue-500/20">
                <p class="text-[11px] font-black text-emerald-500 mb-2 tracking-widest uppercase">02. GHOST MEDIA</p>
                <p class="text-xs opacity-40 uppercase">Hidden Links</p>
            </div>
            <div onclick="setE('/api/trending', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                <p class="text-[11px] font-black text-orange-500 mb-2 tracking-widest uppercase">03. TRENDING</p>
                <p class="text-xs opacity-40 uppercase">Popular Releases</p>
            </div>
            <div onclick="setE('/api/categories', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                <p class="text-[11px] font-black text-purple-500 mb-2 tracking-widest uppercase">04. GENRES</p>
                <p class="text-xs opacity-40 uppercase">8+ Deep Nodes</p>
            </div>
        </div>

        <!-- TESTER BOX -->
        <div class="glass-3d rounded-[60px] p-10 md:p-16 mb-32">
            <h2 id="e-name" class="text-3xl font-black mb-12 uppercase italic tracking-tighter">/api/search</h2>
            <div class="grid md:grid-cols-2 gap-10 mb-10">
                <div><label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">SILENT_KEY</label>
                <input id="key-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition text-sm" value="silent"></div>
                <div><label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">REQUEST_PARAM</label>
                <input id="param-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition text-sm"></div>
            </div>
            <button onclick="run()" class="transmit-btn w-full py-6 rounded-[30px] font-black text-sm tracking-[10px] uppercase active:scale-95 transition-all">Transmit Request</button>
            <div class="response-box mt-12">
                <div class="flex justify-between mb-4"><span id="v-stat" class="text-[10px] font-bold text-blue-500">SERVER: STANDBY</span></div>
                <pre id="json-out">READY FOR COMMANDS...</pre>
            </div>
        </div>

        <!-- STACKED DOCUMENTATION -->
        <h2 class="text-5xl font-black italic uppercase tracking-tighter mb-16">Documentation</h2>
        
        <div class="doc-section">
            <p class="text-blue-500 font-black text-xs mb-6 uppercase italic tracking-[3px]">01. Python (Silent Scraper Node)</p>
            <div class="response-box text-blue-100/60"><pre>import requests\n\nurl = 'https://silent-movies-api.vercel.app/api/search'\nres = requests.get(url, params={'q': 'Spider', 'key': 'silent'})\nprint(res.json())</pre></div>
        </div>

        <div class="doc-section">
            <p class="text-emerald-500 font-black text-xs mb-6 uppercase italic tracking-[3px]">02. Node.js (Async Ghost Request)</p>
            <div class="response-box text-blue-100/60"><pre>const fetch = require('node-fetch');\n\nconst getMovies = async () => {\n  const res = await fetch('.../api/search?q=Spider&key=silent');\n  const data = await res.json();\n  console.log(data);\n}</pre></div>
        </div>

        <div class="doc-section">
            <p class="text-orange-500 font-black text-xs mb-6 uppercase italic tracking-[3px]">03. PHP (Deep Link Stream)</p>
            <div class="response-box text-blue-100/60"><pre>&lt;?php\n$data = file_get_contents('.../api/search?q=Spider&key=silent');\necho $data;\n?&gt;</pre></div>
        </div>

        <footer class="mt-40 text-center pb-24 opacity-20 text-[10px] font-black uppercase tracking-[20px]">
            All Rights Reserved to SILENT TECH | Made with Middle Finger 🖕
        </footer>
    </div>

    <script>
        let ep = '/api/search';
        function setE(e, d) { ep = e; document.getElementById('e-name').innerText = e; document.getElementById('param-in').value = d; }
        async function run() {
            const out = document.getElementById('json-out');
            const k = document.getElementById('key-in').value;
            const p = document.getElementById('param-in').value;
            out.innerText = "Transmitting to Silent Tech Ghost Cluster...";
            let url = ep + '?key=' + k;
            if(ep.includes('search')) url += '&q=' + p;
            if(ep.includes('media')) url += '&slug=' + p;
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
                document.getElementById('v-stat').innerText = "SERVER: DATA_RECEIVED";
            } catch(e) { out.innerText = "TIMEOUT_ERROR"; }
        }
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC (JSON PROP CRAWLER ENGINE) ---

@app.get("/", response_class=HTMLResponse)
def index(): return HTML_UI

@app.get("/api/search")
def search(q: str, key: str = "silent"):
    validate(key)
    res = session.get(f"{BASE}/search?q={q}", headers=HEADERS)
    
    # NEW: Crawler for movies in Next.js hidden JSON
    movies = []
    # Pattern 1: Raw HTML slugs
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    if slugs:
        for s in list(set(slugs)):
            movies.append({"title": s.replace('-', ' ').title(), "slug": s})
            
    # Pattern 2: __NEXT_DATA__ block (Deep Crawler)
    if not movies:
        next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
        if next_data:
            try:
                data = json.loads(next_data.group(1))
                # Drill through typical Next.js structures
                items = data['props']['pageProps'].get('results', []) or data['props']['pageProps'].get('movies', [])
                for item in items:
                    movies.append({"title": item.get('title'), "slug": item.get('slug') or item.get('detailPath')})
            except: pass

    return {"provider": "SILENT TECH", "results": movies}

@app.get("/api/media")
def media(slug: str, request: Request, key: str = "silent"):
    validate(key)
    response = session.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    
    # Deep-Tissue ID extraction
    num_id = None
    # 1. Search in props
    next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text)
    if next_data:
        try:
            parsed = json.loads(next_data.group(1))
            movie_obj = parsed['props']['pageProps'].get('movie', {})
            num_id = movie_obj.get('id')
        except: pass
        
    # 2. Aggressive Regex (User's Colab Logic)
    if not num_id:
        id_patterns = [r'"id":"(\d{15,20})"', r'id=(\d{15,20})', r'\"id\"\:\"(\d+)\"']
        for pattern in id_patterns:
            match = re.search(pattern, response.text)
            if match:
                num_id = match.group(1)
                break
    
    # 3. Last stand: scan raw text for 19-digit number
    if not num_id:
        ids = re.findall(r'(\d{19})', response.text)
        if ids: num_id = ids[0]

    if not num_id:
        return {"error": "Metadata error.", "tip": "Node failed to extract ID."}

    # Fetch sources with Referer requirement
    source_url = f"{BASE}/api/sources?id={num_id}&detailPath={slug}"
    s_res = session.get(source_url, headers={**HEADERS, "referer": f"{BASE}/movie/{slug}"})
    raw_data = s_res.json()

    # Ghost Proxying Links
    if "results" in raw_data:
        for item in raw_data["results"]:
            if "stream_url" in item:
                item["stream_url"] = create_ghost_link(item["stream_url"], request)
            if "download_url" in item:
                item["download_url"] = create_ghost_link(item["download_url"], request)
    
    return {"provider": "SILENT TECH", "ghost_id": num_id, "data": raw_data}

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = session.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/categories")
def categories(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "list": ["Action", "Horror", "Comedy", "Sci-Fi", "Crime", "Animation", "Drama"]}

@app.get("/api/status")
def status(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "engine": "Ghost Core v14 GodMode"}
