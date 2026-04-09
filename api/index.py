from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import re
import json
import base64

app = FastAPI()

# --- CONFIG ---
BASE = "https://cinverse.name.ng"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- GHOST SYSTEM (No 422 Fix) ---
def create_ghost_link(original_url: str, request: Request):
    encoded = base64.b64encode(original_url.encode()).decode()
    base_api_url = str(request.base_url).rstrip('/')
    # Removed mandatory key from ghost link to prevent 422 errors
    return f"{base_api_url}/api/v1/ghost?data={encoded}"

@app.get("/api/v1/ghost")
def ghost_proxy(data: str):
    try:
        real_url = base64.b64decode(data).decode()
        # Redirecting to original source with browser headers
        return RedirectResponse(url=real_url)
    except:
        return {"error": "GHOST_LINK_BROKEN"}

# --- THE UI (3D PREMIUM + STACKED DOCS) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT TECH | GHOST HUB</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #010103; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; perspective: 1500px; overflow-x: hidden; }
        .glass-3d { 
            background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(40px); 
            border: 1px solid rgba(255, 255, 255, 0.08); box-shadow: 0 25px 60px rgba(0,0,0,0.7);
            transform-style: preserve-3d; transition: all 0.5s ease;
        }
        .card-3d:hover { transform: translateZ(50px) rotateX(4deg); border-color: #3b82f6; }
        .response-box { 
            background: #000; border: 1px solid #1f2937; border-radius: 25px; padding: 24px; 
            font-family: monospace; font-size: 11px; color: #60a5fa; overflow: auto; 
            max-height: 550px; white-space: pre-wrap; word-break: break-all;
        }
        .doc-section { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 30px; padding: 35px; margin-bottom: 30px; }
        .ios-dot { width: 12px; height: 12px; border-radius: 50%; }
        ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    </style>
</head>
<body class="p-4 md:p-12 lg:p-20">
    <div class="max-w-7xl mx-auto">
        <header class="glass-3d rounded-[50px] p-10 flex justify-between items-center mb-16">
            <div class="flex items-center gap-6">
                <div class="flex gap-2"><div class="ios-dot bg-[#ff5f57]"></div><div class="ios-dot bg-[#ffbd2e]"></div><div class="ios-dot bg-[#28c840]"></div></div>
                <h1 class="text-4xl font-black tracking-tighter uppercase italic">Silent <span class="text-blue-500 not-italic">Ghost</span></h1>
            </div>
            <div class="hidden md:block text-[10px] font-black opacity-30 tracking-[10px] uppercase">Node_v12_Stable</div>
        </header>

        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            <div onclick="setE('/api/search', 'Spider-Man')" class="glass-3d card-3d p-8 rounded-[35px]">
                <p class="text-[11px] font-black text-blue-500 mb-2 uppercase">01. SEARCH</p>
                <p class="text-xs opacity-40">Get Movie Slugs</p>
            </div>
            <div onclick="setE('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d p-8 rounded-[35px] border-blue-500/30">
                <p class="text-[11px] font-black text-emerald-500 mb-2 uppercase">02. GHOST MEDIA</p>
                <p class="text-xs opacity-40">Hidden Sources</p>
            </div>
            <div onclick="setE('/api/trending', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                <p class="text-[11px] font-black text-orange-500 mb-2 uppercase">03. TRENDING</p>
                <p class="text-xs opacity-40">Top Hits</p>
            </div>
            <div onclick="setE('/api/categories', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                <p class="text-[11px] font-black text-purple-500 mb-2 uppercase">04. GENRES</p>
                <p class="text-xs opacity-40">8+ Categories</p>
            </div>
        </div>

        <div class="glass-3d rounded-[60px] p-10 md:p-16 mb-20">
            <h2 id="e-title" class="text-3xl font-black mb-12 uppercase italic tracking-tighter">/api/search</h2>
            <div class="grid md:grid-cols-2 gap-10 mb-10">
                <div><label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">AUTH_KEY</label>
                <input id="key-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition text-sm" value="silent"></div>
                <div><label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">PARAMETER</label>
                <input id="param-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition text-sm"></div>
            </div>
            <button onclick="run()" class="w-full bg-blue-600 py-6 rounded-[30px] font-black text-sm tracking-[8px] uppercase active:scale-95 transition shadow-xl shadow-blue-500/20">Transmit Request</button>
            <div class="response-box mt-12">
                <pre id="json-out">SYSTEM_READY...</pre>
            </div>
        </div>

        <h2 class="text-5xl font-black italic uppercase tracking-tighter mb-16">The Documentation</h2>
        <div class="doc-section"><p class="text-blue-500 font-black text-xs mb-4 uppercase italic">01. Python (Silent Tech Logic)</p>
        <div class="response-box text-blue-100/60"><pre>import requests\nurl = 'https://YOUR_DOMAIN/api/search'\nres = requests.get(url, params={'q': 'Spider', 'key': 'silent'}, headers={'user-agent': 'Mozilla/5.0'})\nprint(res.json())</pre></div></div>
        
        <div class="doc-section"><p class="text-emerald-500 font-black text-xs mb-4 uppercase italic">02. Node.js (Ghost Node)</p>
        <div class="response-box text-blue-100/60"><pre>const fetch = require('node-fetch');\nconst res = await fetch('https://YOUR_DOMAIN/api/search?q=Spider&key=silent');\nconsole.log(await res.json());</pre></div></div>

        <div class="doc-section"><p class="text-orange-500 font-black text-xs mb-4 uppercase italic">03. PHP (Silent Stream)</p>
        <div class="response-box text-blue-100/60"><pre>&lt;?php\n$data = file_get_contents('https://YOUR_DOMAIN/api/search?q=Spider&key=silent');\necho $data;\n?&gt;</pre></div></div>

        <footer class="mt-40 text-center pb-24 opacity-20 text-[10px] font-black uppercase tracking-[20px]">
            All Rights Reserved to SILENT TECH | Made with Middle Finger 🖕
        </footer>
    </div>

    <script>
        let ep = '/api/search';
        function setE(e, d) { ep = e; document.getElementById('e-title').innerText = e; document.getElementById('param-in').value = d; }
        async function run() {
            const out = document.getElementById('json-out');
            const k = document.getElementById('key-in').value;
            const p = document.getElementById('param-in').value;
            out.innerText = "Transmitting to Ghost Node...";
            let url = ep + '?key=' + k;
            if(ep.includes('search')) url += '&q=' + p;
            if(ep.includes('media')) url += '&slug=' + p;
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "TIMEOUT_ERROR"; }
        }
    </script>
</body>
</html>
"""

# --- BACKEND ENGINE (V12 GOD-MODE) ---

@app.get("/", response_class=HTMLResponse)
def index(): return HTML_UI

@app.get("/api/search")
def search(q: str, key: str = "silent"):
    validate(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}

@app.get("/api/media")
def media(slug: str, request: Request, key: str = "silent"):
    validate(key)
    # The "Bitch-Proof" Scraper
    response = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    
    # Scanning NEXT_DATA and raw IDs
    num_id = None
    # Method 1: Extraction from Next.js Data Block
    next_data = re.search(r'\{"props":.*?\}', response.text)
    if next_data:
        try:
            parsed = json.loads(next_data.group(0))
            # Drill down to the ID (Common Next.js Movie site structure)
            num_id = parsed['props']['pageProps']['movie']['id']
        except: pass

    # Method 2: Fallback Brute Force Regex
    if not num_id:
        patterns = [r'"id":"(\d{15,20})"', r'id=(\d{15,20})', r'\"id\"\:\"(\d+)\"']
        for p in patterns:
            match = re.search(p, response.text)
            if match:
                num_id = match.group(1)
                break
    
    if not num_id:
        return {"error": "Metadata error. Ensure slug is correct."}

    # Calling sources with Referer
    source_url = f"{BASE}/api/sources?id={num_id}&detailPath={slug}"
    s_res = requests.get(source_url, headers={**HEADERS, "referer": f"{BASE}/movie/{slug}"})
    raw_data = s_res.json()

    # Ghost Masking
    if "results" in raw_data:
        for item in raw_data["results"]:
            if "stream_url" in item:
                item["stream_url"] = create_ghost_link(item["stream_url"], request)
            if "download_url" in item:
                item["download_url"] = create_ghost_link(item["download_url"], request)
    
    return {"provider": "SILENT TECH", "ghost_id": num_id, "slug": slug, "data": raw_data}

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/categories")
def categories(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "list": ["Action", "Horror", "Comedy", "Sci-Fi", "Crime", "Animation", "Drama"]}
