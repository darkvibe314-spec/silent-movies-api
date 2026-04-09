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
    "referer": BASE
}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- THE PREMIUM 3D UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT PRO | API HUB</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #030305; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; perspective: 1200px; overflow-x: hidden; }
        .glass-3d { 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(25px); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }
        .card-3d { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); cursor: pointer; }
        .card-3d:hover { transform: translateZ(20px) translateY(-5px); border-color: #3b82f6; }
        .response-area { 
            background: #000; border: 1px solid #1f2937; border-radius: 20px; 
            padding: 20px; font-family: 'Courier New', monospace; font-size: 11px; 
            color: #60a5fa; overflow: auto; max-height: 500px;
            white-space: pre-wrap; word-break: break-all;
        }
        .doc-block { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; margin-bottom: 20px; }
        ::-webkit-scrollbar { width: 5px; } ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    </style>
</head>
<body class="p-4 md:p-12">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER -->
        <header class="glass-3d rounded-[40px] p-8 flex justify-between items-center mb-12">
            <div class="flex items-center gap-6">
                <div class="flex gap-2">
                    <div class="w-3 h-3 bg-[#ff5f57] rounded-full"></div>
                    <div class="w-3 h-3 bg-[#ffbd2e] rounded-full"></div>
                    <div class="w-3 h-3 bg-[#28c840] rounded-full"></div>
                </div>
                <h1 class="text-3xl font-black tracking-tighter uppercase italic">Silent <span class="text-blue-500 not-italic">API</span></h1>
            </div>
            <div class="text-[10px] font-black opacity-30 tracking-[5px] uppercase">Node_v6_Stable</div>
        </header>

        <!-- PLAYGROUND -->
        <div class="space-y-10">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div onclick="setE('/api/search', 'Spider-Man')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-blue-500 mb-1">01. SEARCH</p>
                    <p class="text-xs opacity-40 uppercase">Find Slugs</p>
                </div>
                <div onclick="setE('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-emerald-500 mb-1">02. DOWNLOAD</p>
                    <p class="text-xs opacity-40 uppercase">Video Links</p>
                </div>
                <div onclick="setE('/api/trending', 'N/A')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-orange-500 mb-1">03. TRENDING</p>
                    <p class="text-xs opacity-40 uppercase">Top Hits</p>
                </div>
                <div onclick="setE('/api/categories', 'N/A')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-purple-500 mb-1">04. GENRES</p>
                    <p class="text-xs opacity-40 uppercase">8+ Categories</p>
                </div>
            </div>

            <div class="glass-3d rounded-[45px] p-8 md:p-12">
                <h2 id="end-title" class="text-2xl font-black mb-8 uppercase italic tracking-tighter">/api/search</h2>
                <div class="grid md:grid-cols-2 gap-8 mb-8">
                    <div>
                        <label class="text-[10px] font-black opacity-30 mb-3 block tracking-[2px]">AUTH_KEY</label>
                        <input id="in-k" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition" value="silent">
                    </div>
                    <div>
                        <label class="text-[10px] font-black opacity-30 mb-3 block tracking-[2px]">PARAMETER</label>
                        <input id="in-p" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition">
                    </div>
                </div>
                <button onclick="run()" class="w-full bg-blue-600 hover:bg-blue-500 py-5 rounded-2xl font-black text-sm tracking-[5px] uppercase transition shadow-lg shadow-blue-500/20">Execute Request</button>
                
                <div class="response-area mt-10">
                    <div class="flex justify-between mb-4"><span class="text-[10px] font-bold text-blue-500 uppercase">Live Result Viewer</span></div>
                    <pre id="out">Standing by...</pre>
                </div>
            </div>
        </div>

        <!-- DOCUMENTATION (STACKED) -->
        <div class="mt-20 space-y-10">
            <h2 class="text-4xl font-black italic uppercase tracking-tighter">Documentation</h2>
            
            <div class="doc-block">
                <p class="text-blue-500 font-bold text-xs mb-4">PYTHON (REQUESTS)</p>
                <pre class="text-[11px] opacity-70">import requests\nurl = 'https://YOUR_DOMAIN/api/search?q=Spider&key=silent'\nprint(requests.get(url).json())</pre>
            </div>

            <div class="doc-block">
                <p class="text-yellow-500 font-bold text-xs mb-4">NODE.JS (FETCH)</p>
                <pre class="text-[11px] opacity-70">const res = await fetch('https://YOUR_DOMAIN/api/search?q=Spider&key=silent');\nconst data = await res.json();\nconsole.log(data);</pre>
            </div>

            <div class="doc-block">
                <p class="text-emerald-500 font-bold text-xs mb-4">PHP (CURL)</p>
                <pre class="text-[11px] opacity-70">&lt;?php\n$data = file_get_contents('https://YOUR_DOMAIN/api/search?q=Spider&key=silent');\necho $data;\n?&gt;</pre>
            </div>
        </div>

        <footer class="mt-32 text-center pb-20">
            <p class="text-[9px] tracking-[15px] opacity-20 font-black uppercase">All Rights Reserved to SILENT TECH | Made with Middle Finger 🖕</p>
        </footer>
    </div>

    <script>
        let cur = '/api/search';
        function setE(e, d) { cur = e; document.getElementById('end-title').innerText = e; document.getElementById('in-p').value = d; }

        async function run() {
            const out = document.getElementById('out');
            const k = document.getElementById('in-k').value;
            const p = document.getElementById('in-p').value;
            out.innerText = "Connecting to Silent Tech Node...";
            let url = cur + '?key=' + k;
            if(cur.includes('search')) url += '&q=' + p;
            if(cur.includes('media')) url += '&slug=' + p;
            
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "Connection Failed."; }
        }
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC ---

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
    page = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    # Aggressive ID Search
    num_id = re.search(r'"id":"(\d{15,20})"', page.text)
    if not num_id: num_id = re.search(r'\"id\"\:\"(\d+)\"', page.text)
    if not num_id:
        num_id = re.search(r'"(\d{18,20})"', page.text)
    
    if not num_id: return {"error": "Metadata error."}

    source_url = f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}"
    res = requests.get(source_url, headers={**HEADERS, "referer": f"{BASE}/movie/{slug}"})
    
    # We return the REAL links so they actually work, but label them SILENT TECH
    return {"provider": "SILENT TECH", "id": num_id.group(1), "slug": slug, "data": res.json()}

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
    return {"provider": "SILENT TECH", "engine": "Premium Core V7 Stable"}
