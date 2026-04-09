from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import re
import json
import base64

app = FastAPI()

# --- ENGINE CONFIG ---
BASE = "https://cinverse.name.ng"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "referer": BASE
}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- GHOST LINK LOGIC ---
def encode_ghost(url: str, request: Request):
    """Hides the original provider behind a base64 string"""
    encoded = base64.b64encode(url.encode()).decode()
    base = str(request.base_url).rstrip('/')
    return f"{base}/api/v1/ghost?data={encoded}&key=silent"

@app.get("/api/v1/ghost")
def ghost_redirect(data: str, key: str):
    """The Ghost Proxy: Decodes and redirects to the source secretly"""
    validate(key)
    try:
        real_url = base64.b64decode(data).decode()
        return RedirectResponse(url=real_url)
    except:
        raise HTTPException(status_code=400, detail="INVALID_GHOST_STREAM")

# --- PREMIUM 3D RESPONSIVE UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT TECH | GHOST NODE</title>
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
        .doc-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 30px; padding: 30px; margin-bottom: 30px; }
        ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    </style>
</head>
<body class="p-4 md:p-12 lg:p-20">
    <div class="max-w-7xl mx-auto">
        <header class="glass-3d rounded-[50px] p-10 flex justify-between items-center mb-16">
            <h1 class="text-4xl font-black tracking-tighter uppercase italic">Silent <span class="text-blue-500 not-italic">Ghost</span></h1>
            <div class="hidden md:block text-[10px] font-black opacity-30 tracking-[10px] uppercase">Node_v11_Ghost_Mode</div>
        </header>

        <!-- PLAYGROUND -->
        <div class="space-y-12 mb-24">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
                <div onclick="setE('/api/search', 'Spider-Man')" class="glass-3d card-3d p-8 rounded-[35px]">
                    <p class="text-[11px] font-black text-blue-500 mb-2 uppercase tracking-widest">01. SEARCH</p>
                    <p class="text-xs opacity-40">Fetch Movie Slugs</p>
                </div>
                <div onclick="setE('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d p-8 rounded-[35px] border-blue-500/30">
                    <p class="text-[11px] font-black text-emerald-500 mb-2 uppercase tracking-widest">02. GHOST MEDIA</p>
                    <p class="text-xs opacity-40">Direct Movie Links</p>
                </div>
                <div onclick="setE('/api/trending', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                    <p class="text-[11px] font-black text-orange-500 mb-2 uppercase tracking-widest">03. TRENDING</p>
                    <p class="text-sm opacity-40">Top Worldwide Hits</p>
                </div>
                <div onclick="setE('/api/categories', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                    <p class="text-[11px] font-black text-purple-500 mb-2 uppercase tracking-widest">04. CATEGORIES</p>
                    <p class="text-sm opacity-40">8+ Genre Scraper</p>
                </div>
            </div>

            <div class="glass-3d rounded-[60px] p-10 md:p-16">
                <h2 id="end-title" class="text-3xl font-black mb-12 uppercase italic tracking-tighter">/api/search</h2>
                <div class="grid md:grid-cols-2 gap-10 mb-10">
                    <div><label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">SILENT_KEY</label>
                    <input id="key-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition" value="silent"></div>
                    <div><label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">PARAM_VALUE</label>
                    <input id="param-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition"></div>
                </div>
                <button onclick="run()" class="w-full bg-blue-600 py-6 rounded-[30px] font-black text-sm tracking-[8px] uppercase active:scale-95 transition-all shadow-xl shadow-blue-500/20">Transmit Request</button>
                <div class="response-area mt-12">
                    <div class="flex justify-between mb-4"><span class="text-[10px] font-bold text-blue-500 uppercase">Live Output</span></div>
                    <pre id="json-out">READY FOR COMMANDS...</pre>
                </div>
            </div>
        </div>

        <!-- STACKED DOCS -->
        <h2 class="text-5xl font-black italic uppercase tracking-tighter mb-16">The Documentation</h2>
        <div class="doc-card">
            <p class="text-blue-500 font-black text-xs mb-4 uppercase tracking-widest italic">01. Python (Requests Node)</p>
            <div class="response-area text-blue-100/60"><pre>import requests\n\nurl = 'https://YOUR_DOMAIN/api/search'\nres = requests.get(url, params={'q': 'Spider', 'key': 'silent'})\nprint(res.json())</pre></div>
        </div>
        
        <div class="doc-card">
            <p class="text-emerald-500 font-black text-xs mb-4 uppercase tracking-widest italic">02. Node.js (Async Node)</p>
            <div class="response-area text-blue-100/60"><pre>const fetch = require('node-fetch');\n\nconst getMovies = async () => {\n  const res = await fetch('.../api/search?q=Spider&key=silent');\n  console.log(await res.json());\n}</pre></div>
        </div>

        <div class="doc-card">
            <p class="text-orange-500 font-black text-xs mb-4 uppercase tracking-widest italic">03. PHP (Ghost File Stream)</p>
            <div class="response-area text-blue-100/60"><pre>&lt;?php\n$data = file_get_contents('.../api/search?q=Spider&key=silent');\necho $data;\n?&gt;</pre></div>
        </div>

        <footer class="mt-40 text-center pb-24 opacity-20 text-[10px] font-black uppercase tracking-[20px]">
            All Rights Reserved to SILENT TECH | Made with Middle Finger 🖕
        </footer>
    </div>

    <script>
        let ep = '/api/search';
        function setE(e, d) { ep = e; document.getElementById('end-title').innerText = e; document.getElementById('param-in').value = d; }
        async function run() {
            const out = document.getElementById('json-out');
            const k = document.getElementById('key-in').value;
            const p = document.getElementById('param-in').value;
            out.innerText = "Connecting to Silent Tech Cluster...";
            let url = ep + '?key=' + k;
            if(ep.includes('search')) url += '&q=' + p;
            if(ep.includes('media')) url += '&slug=' + p;
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "Error Connecting to Node."; }
        }
    </script>
</body>
</html>
"""

# --- BACKEND API LOGIC ---

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
    # 1. Scrape Movie Page for Numeric ID
    page = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    
    # Aggressive ID Matcher
    num_id = re.search(r'"id":"(\d{15,20})"', page.text)
    if not num_id: num_id = re.search(r'\"id\"\:\"(\d+)\"', page.text)
    if not num_id:
        ids = re.findall(r'"(\d{18,20})"', page.text)
        if ids: num_id = type('Match', (object,), {'group': lambda x: ids[0]})

    if not num_id: return {"error": "Metadata error."}

    # 2. Get Real Sources with Mandatory Referer
    sources_url = f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}"
    res = requests.get(sources_url, headers={**HEADERS, "referer": f"{BASE}/movie/{slug}"})
    raw_data = res.json()

    # 3. Apply Ghost Masking to Results
    if "results" in raw_data:
        for item in raw_data["results"]:
            if "stream_url" in item:
                item["stream_url"] = encode_ghost(item["stream_url"], request)
            if "download_url" in item:
                item["download_url"] = encode_ghost(item["download_url"], request)

    return {"provider": "SILENT TECH", "slug": slug, "data": raw_data}

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/categories")
def categories(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "list": ["Action", "Horror", "Comedy", "Sci-Fi", "Crime", "Animation", "Drama", "Documentary"]}

@app.get("/api/status")
def status(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "status": "Online", "engine": "Ghost v11 Stable"}
