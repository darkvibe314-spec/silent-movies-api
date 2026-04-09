from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import requests
import re
import json

app = FastAPI()

# --- ENGINE CONFIG ---
BASE = "https://cinverse.name.ng"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "referer": BASE
}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- THE PREMIUM 3D RESPONSIVE UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT PRO | MOVIE API HUB</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #010103; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; perspective: 1500px; overflow-x: hidden; }
        .glass-3d { 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(40px); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            box-shadow: 0 25px 60px rgba(0,0,0,0.7);
            transform-style: preserve-3d;
            transition: all 0.5s ease;
        }
        .card-3d:hover { 
            transform: translateZ(50px) rotateX(4deg) rotateY(-4deg); 
            border-color: #3b82f6; 
            background: rgba(59, 130, 246, 0.05);
        }
        .ios-dot { width: 12px; height: 12px; border-radius: 50%; }
        .response-box { 
            background: #000; border: 1px solid #1f2937; border-radius: 25px; 
            padding: 24px; font-family: 'Courier New', monospace; font-size: 11px; 
            color: #60a5fa; overflow: auto; max-height: 550px;
            white-space: pre-wrap; word-break: break-all;
        }
        .doc-section { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 25px; padding: 25px; margin-bottom: 25px; }
        ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
        .glow-btn { 
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            box-shadow: 0 10px 20px rgba(59, 130, 246, 0.4);
        }
    </style>
</head>
<body class="p-4 md:p-12 lg:p-20">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER 3D -->
        <header class="glass-3d rounded-[50px] p-10 flex justify-between items-center mb-16">
            <div class="flex items-center gap-6">
                <div class="flex gap-2">
                    <div class="ios-dot bg-[#ff5f57]"></div><div class="ios-dot bg-[#ffbd2e]"></div><div class="ios-dot bg-[#28c840]"></div>
                </div>
                <h1 class="text-4xl font-black tracking-tighter uppercase italic">Silent <span class="text-blue-500 not-italic">Platform</span></h1>
            </div>
            <div class="hidden md:block text-[10px] font-black opacity-30 tracking-[8px] uppercase">Node_v9_God_Mode</div>
        </header>

        <!-- PLAYGROUND -->
        <div class="space-y-12">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
                <div onclick="setEndpoint('/api/search', 'Spider-Man')" class="glass-3d card-3d p-8 rounded-[35px]">
                    <p class="text-[11px] font-black text-blue-500 mb-2 uppercase tracking-widest">01. SEARCH</p>
                    <p class="text-sm opacity-40">Fetch Movie Slugs</p>
                </div>
                <div onclick="setEndpoint('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d p-8 rounded-[35px] border-blue-500/30">
                    <p class="text-[11px] font-black text-emerald-500 mb-2 uppercase tracking-widest">02. SOURCES</p>
                    <p class="text-sm opacity-40">Direct Media Links</p>
                </div>
                <div onclick="setEndpoint('/api/trending', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                    <p class="text-[11px] font-black text-orange-500 mb-2 uppercase tracking-widest">03. TRENDING</p>
                    <p class="text-sm opacity-40">Global Releases</p>
                </div>
                <div onclick="setEndpoint('/api/categories', 'N/A')" class="glass-3d card-3d p-8 rounded-[35px]">
                    <p class="text-[11px] font-black text-purple-500 mb-2 uppercase tracking-widest">04. CATEGORIES</p>
                    <p class="text-sm opacity-40">Genre Scraper</p>
                </div>
            </div>

            <div class="glass-3d rounded-[60px] p-10 md:p-16">
                <h2 id="endpoint-name" class="text-3xl font-black mb-12 uppercase italic tracking-tighter">/api/search</h2>
                <div class="grid md:grid-cols-2 gap-10 mb-10">
                    <div>
                        <label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">SILENT_AUTH_KEY</label>
                        <input id="key-val" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition text-sm" value="silent">
                    </div>
                    <div>
                        <label class="text-[11px] font-black opacity-30 mb-4 block tracking-[3px]">REQUEST_PARAM</label>
                        <input id="param-val" class="w-full bg-black/40 border border-white/10 rounded-2xl p-5 outline-none focus:border-blue-500 transition text-sm">
                    </div>
                </div>
                <button onclick="execute()" class="glow-btn w-full py-6 rounded-[30px] font-black text-sm tracking-[8px] uppercase active:scale-95 transition-all">Transmit Request</button>
                
                <div class="response-box mt-12">
                    <div class="flex justify-between mb-6"><span class="text-[11px] font-bold text-blue-500 tracking-[2px] uppercase">Node Server Response</span></div>
                    <pre id="json-out">SYSTEM_READY...</pre>
                </div>
            </div>
        </div>

        <!-- DOCUMENTATION (STACKED PREMIUM) -->
        <div class="mt-32 space-y-12">
            <h2 class="text-5xl font-black italic uppercase tracking-tighter mb-16">The Documentation</h2>
            
            <div class="doc-section">
                <p class="text-blue-500 font-black text-xs mb-6 tracking-widest uppercase italic">01. Python (Requests Engine)</p>
                <div class="response-box text-blue-100/60">
                    <pre>import requests\n\nurl = 'https://silent-movies-api.vercel.app/api/search'\nparams = {'q': 'Spider', 'key': 'silent'}\n\nresponse = requests.get(url, params=params)\nprint(response.json())</pre>
                </div>
            </div>

            <div class="doc-section">
                <p class="text-emerald-500 font-black text-xs mb-6 tracking-widest uppercase italic">02. Node.js (Async Fetch)</p>
                <div class="response-box text-blue-100/60">
                    <pre>const fetch = require('node-fetch');\n\nasync function getSilentMovies() {\n  const url = 'https://silent-movies-api.vercel.app/api/search?q=Spider&key=silent';\n  const res = await fetch(url);\n  const data = await res.json();\n  console.log(data);\n}\n\ngetSilentMovies();</pre>
                </div>
            </div>

            <div class="doc-section">
                <p class="text-orange-500 font-black text-xs mb-6 tracking-widest uppercase italic">03. PHP (File Get Contents)</p>
                <div class="response-box text-blue-100/60">
                    <pre>&lt;?php\n$q = 'Spider';\n$key = 'silent';\n$url = 'https://silent-movies-api.vercel.app/api/search?q='.$q.'&key='.$key;\n\n$response = file_get_contents($url);\necho $response;\n?&gt;</pre>
                </div>
            </div>
        </div>

        <footer class="mt-40 text-center pb-24">
            <p class="text-[10px] tracking-[20px] opacity-20 font-black uppercase">All Rights Reserved to SILENT TECH | Made with Middle Finger 🖕</p>
        </footer>
    </div>

    <script>
        let endpoint = '/api/search';
        function setEndpoint(e, d) { endpoint = e; document.getElementById('endpoint-name').innerText = e; document.getElementById('param-val').value = d; }

        async function execute() {
            const out = document.getElementById('json-out');
            const k = document.getElementById('key-val').value;
            const p = document.getElementById('param-val').value;
            out.innerText = "Connecting to Silent Tech Node v9...";
            let url = endpoint + '?key=' + k;
            if(endpoint.includes('search')) url += '&q=' + p;
            if(endpoint.includes('media')) url += '&slug=' + p;
            
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "CRITICAL_NODE_TIMEOUT_ERROR"; }
        }
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC (GOD-MODE SCRAPER) ---

@app.get("/", response_class=HTMLResponse)
def index(): return HTML_UI

@app.get("/api/search")
def search(q: str, key: str = "silent"):
    validate(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}

@app.get("/api/media")
def media(slug: str, key: str = "silent"):
    validate(key)
    # Step 1: Visit movie page with aggressive numeric ID scraper
    movie_page = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    
    # Brute-force ID search across the entire HTML source
    id_match = re.search(r'"id":"(\d{15,20})"', movie_page.text)
    if not id_match:
        id_match = re.search(r'\"id\"\:\"(\d+)\"', movie_page.text)
    if not id_match:
        id_match = re.search(r'id=(\d{15,20})', movie_page.text)
    if not id_match:
        # Final stand: hunt for any 19-digit numeric string in the hydration props
        ids = re.findall(r'"(\d{18,20})"', movie_page.text)
        if ids: id_match = type('Match', (object,), {'group': lambda x: ids[0]})

    if not id_match:
        return {"error": "Metadata error.", "tip": "Node failed to extract numeric ID. The site might have updated its Next.js build."}

    num_id = id_match.group(1)

    # Step 2: Use the ID to get sources (CRITICAL: Needs Referer for Links)
    source_url = f"{BASE}/api/sources?id={num_id}&detailPath={slug}"
    # We must pretend we are coming directly from the movie page to unlock the links
    res = requests.get(source_url, headers={**HEADERS, "referer": f"{BASE}/movie/{slug}"})
    
    # We return the REAL URLs so the links actually work for your users
    return {
        "provider": "SILENT TECH", 
        "id": num_id, 
        "slug": slug, 
        "data": res.json()
    }

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
    return {"provider": "SILENT TECH", "engine": "Premium Core v9 - God Mode Enabled"}
