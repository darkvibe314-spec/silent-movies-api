from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import requests
import re
import json

app = FastAPI()

# --- ENGINE CONFIG ---
BASE = "https://cinverse.name.ng"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "referer": BASE,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

def mask_data(data):
    """Deep scrubs external branding and replaces it with SILENT TECH nodes"""
    str_data = json.dumps(data)
    # Masking external servers
    str_data = str_data.replace("gzmovieboxapi.septorch.tech", "api.silent-node.tech")
    str_data = str_data.replace("hakunaymatata.com", "cdn.silent-server.xyz")
    # Masking keys in URLs
    str_data = re.sub(r'apikey=[^&"]+', 'apikey=SILENT_MASTER_KEY', str_data)
    return json.loads(str_data)

# --- THE PREMIUM 3D RESPONSIVE UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT TECH | PRO MOVIE API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root { --blue: #3b82f6; --bg: #030305; }
        body { background: var(--bg); color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; perspective: 1000px; overflow-x: hidden; }
        .glass-panel { 
            background: rgba(255, 255, 255, 0.01); 
            backdrop-filter: blur(30px); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            box-shadow: 0 15px 40px rgba(0,0,0,0.6);
            z-index: 10;
        }
        .card-3d { transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; position: relative; z-index: 20; }
        .card-3d:active { transform: scale(0.95); }
        .ios-btn { background: var(--blue); box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4); z-index: 30; }
        .response-box { 
            background: #000; border: 1px solid #1f2937; border-radius: 20px; 
            padding: 20px; font-family: 'Courier New', monospace; font-size: 11px; 
            color: #60a5fa; overflow: auto; max-height: 500px; white-space: pre-wrap; word-break: break-all;
        }
        .nav-active { color: var(--blue); border-bottom: 2px solid var(--blue); }
        .doc-btn { background: rgba(255,255,255,0.05); cursor: pointer; position: relative; z-index: 50; }
        .doc-btn.active { background: var(--blue); box-shadow: 0 0 15px var(--blue); }
        .dot { width: 10px; height: 10px; border-radius: 50%; }
        @media (max-width: 640px) { .grid-mobile { grid-template-columns: repeat(2, 1fr); } }
    </style>
</head>
<body class="p-4 md:p-8">
    <div class="max-w-6xl mx-auto">
        <!-- HEADER -->
        <nav class="glass-panel rounded-[30px] p-6 flex justify-between items-center mb-10">
            <div class="flex items-center gap-4">
                <div class="flex gap-1.5"><div class="dot bg-red-500"></div><div class="dot bg-yellow-500"></div><div class="dot bg-green-500"></div></div>
                <h1 class="text-2xl font-black uppercase tracking-tighter italic">Silent <span class="text-blue-500 not-italic">API</span></h1>
            </div>
            <div class="flex gap-6">
                <button onclick="tab('tester')" id="n-tester" class="text-[10px] font-black uppercase tracking-widest nav-active">Playground</button>
                <button onclick="tab('docs')" id="n-docs" class="text-[10px] font-black uppercase tracking-widest opacity-40">Documentation</button>
            </div>
        </nav>

        <!-- TESTER VIEW -->
        <div id="v-tester" class="space-y-8">
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 grid-mobile">
                <div onclick="setE('/api/search', 'Spider-Man')" class="glass-panel card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-bold text-blue-500 mb-1">01. SEARCH</p>
                    <p class="text-[9px] opacity-40 uppercase">Find Slugs</p>
                </div>
                <div onclick="setE('/api/media', 'the-spider-man-2-mdhIbqhHpT6')" class="glass-panel card-3d p-6 rounded-3xl border-blue-500/20">
                    <p class="text-[10px] font-bold text-emerald-500 mb-1">02. DOWNLOAD</p>
                    <p class="text-[9px] opacity-40 uppercase">Get Sources</p>
                </div>
                <div onclick="setE('/api/trending', 'N/A')" class="glass-panel card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-bold text-orange-500 mb-1">03. TRENDING</p>
                    <p class="text-[9px] opacity-40 uppercase">Top Hits</p>
                </div>
                <div onclick="setE('/api/categories', 'N/A')" class="glass-panel card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-bold text-purple-500 mb-1">04. GENRES</p>
                    <p class="text-[9px] opacity-40 uppercase">8+ Categories</p>
                </div>
            </div>

            <div class="glass-panel rounded-[40px] p-8 md:p-12">
                <h2 id="end-title" class="text-2xl font-black mb-8 uppercase">/api/search</h2>
                <div class="grid md:grid-cols-2 gap-6 mb-8">
                    <div class="space-y-2">
                        <label class="text-[10px] font-black opacity-30 tracking-widest uppercase">Auth Key</label>
                        <input id="in-k" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition" value="silent">
                    </div>
                    <div class="space-y-2">
                        <label class="text-[10px] font-black opacity-30 tracking-widest uppercase">Parameter</label>
                        <input id="in-p" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition" placeholder="slug or query...">
                    </div>
                </div>
                <button onclick="run()" class="ios-btn w-full py-5 rounded-2xl font-black text-sm uppercase tracking-[5px] active:scale-95 transition">Execute Request</button>
                <div class="response-box mt-10">
                    <div class="flex justify-between mb-4"><span class="text-[9px] font-bold text-blue-500 uppercase tracking-widest">Live Server Feed</span></div>
                    <pre id="out">Standing by...</pre>
                </div>
            </div>
        </div>

        <!-- DOCS VIEW -->
        <div id="v-docs" class="hidden space-y-8">
            <div class="glass-panel rounded-[40px] p-10">
                <h2 class="text-3xl font-black mb-10 uppercase italic">Documentation</h2>
                <div class="flex gap-3 mb-8 overflow-x-auto">
                    <button onclick="lang('py')" id="l-py" class="doc-btn px-6 py-3 rounded-xl text-[10px] font-black active">PYTHON</button>
                    <button onclick="lang('js')" id="l-js" class="doc-btn px-6 py-3 rounded-xl text-[10px] font-black">NODE.JS</button>
                    <button onclick="lang('php')" id="l-php" class="doc-btn px-6 py-3 rounded-xl text-[10px] font-black">PHP</button>
                </div>
                <div class="response-box"><pre id="c-out">Select language...</pre></div>
            </div>
        </div>

        <footer class="mt-24 text-center pb-12 opacity-20 text-[9px] font-black uppercase tracking-[10px]">
            ALL RIGHTS RESERVED TO SILENT TECH | MADE WITH MIDDLE FINGER 🖕
        </footer>
    </div>

    <script>
        let cur = '/api/search';
        function setE(e, d) { cur = e; document.getElementById('end-title').innerText = e; document.getElementById('in-p').value = d; }
        
        function tab(v) { 
            document.getElementById('v-tester').style.display = v === 'tester' ? 'block' : 'none'; 
            document.getElementById('v-docs').style.display = v === 'docs' ? 'block' : 'none';
            document.getElementById('n-tester').classList.toggle('nav-active', v==='tester');
            document.getElementById('n-docs').classList.toggle('nav-active', v==='docs');
            if(v==='docs') lang('py');
        }

        async function run() {
            const out = document.getElementById('out');
            const k = document.getElementById('in-k').value;
            const p = document.getElementById('in-p').value;
            out.innerText = "Requesting Silent Tech Node...";
            let url = cur + '?key=' + k;
            if(cur.includes('search')) url += '&q=' + p;
            if(cur.includes('media')) url += '&slug=' + p;
            
            try {
                const r = await fetch(url);
                const d = await r.json();
                out.innerText = JSON.stringify(d, null, 2);
            } catch(e) { out.innerText = "Error: Connection Failed."; }
        }

        const snips = {
            py: "import requests\\nres = requests.get('URL/api/search?q=Spider&key=silent')\\nprint(res.json())",
            js: "fetch('URL/api/search?q=Spider&key=silent')\\n  .then(r => r.json())\\n  .then(console.log)",
            php: "<?php\\n$data = file_get_contents('URL/api/search?q=Spider&key=silent');\\necho $data;\\n?>"
        };

        function lang(l) {
            document.querySelectorAll('.doc-btn').forEach(b => b.classList.remove('active', 'bg-blue-600'));
            const activeBtn = document.getElementById('l-'+l);
            activeBtn.classList.add('active', 'bg-blue-600');
            document.getElementById('c-out').innerText = snips[l];
        }
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC (FIXED ENGINE) ---

@app.get("/", response_class=HTMLResponse)
def index(): return HTML_UI

@app.get("/api/search")
def search(q: str, key: str = "silent"):
    validate(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    # Extract slugs more aggressively
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    data = {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}
    return mask_data(data)

@app.get("/api/media")
def media(slug: str, key: str = "silent"):
    validate(key)
    # Scrape Numeric ID using your exact Colab Logic
    page = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    
    # Colab patterns - prioritized for high accuracy
    id_patterns = [
        r'"id":"(\d{15,20})"', 
        r'id=(\d{15,20})',
        r'movie/.*?(\d{15,20})',
        r'\"id\"\:\"(\d+)\"',
        r'"(\d{18,20})"' # Last resort - look for any long number in quotes
    ]
    
    numeric_id = None
    for pattern in id_patterns:
        match = re.search(pattern, page.text)
        if match:
            numeric_id = match.group(1)
            break

    if not numeric_id:
        return {"error": "Metadata error.", "details": "Node failed to extract numeric ID."}

    # Fetch Real Sources with Mandatory Referer
    source_url = f"{BASE}/api/sources?id={numeric_id}&detailPath={slug}"
    res = requests.get(source_url, headers={**HEADERS, "referer": f"{BASE}/movie/{slug}"})
    
    final_data = {"provider": "SILENT TECH", "slug": slug, "id": numeric_id, "data": res.json()}
    return mask_data(final_data)

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return mask_data({"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]})

@app.get("/api/categories")
def categories(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "list": ["Action", "Horror", "Comedy", "Sci-Fi", "Crime", "Animation", "Drama", "Documentary"]}

@app.get("/api/status")
def status(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "engine": "Premium Hybrid V5 (Stable)"}
