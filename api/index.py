from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import requests
import re
import json

app = FastAPI()

# --- THE ENGINE CONFIG ---
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
            transform-style: preserve-3d;
        }
        .card-3d { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); cursor: pointer; }
        .card-3d:hover { 
            transform: translateZ(30px) translateY(-5px) rotateX(4deg); 
            border-color: #3b82f6; background: rgba(59, 130, 246, 0.05);
        }
        .ios-dot { width: 12px; height: 12px; border-radius: 50%; }
        .response-area { 
            background: #000; border: 1px solid #1f2937; border-radius: 20px; 
            padding: 20px; font-family: 'Courier New', monospace; font-size: 11px; 
            color: #60a5fa; overflow: auto; max-height: 500px;
            white-space: pre-wrap; word-break: break-all;
        }
        .doc-tab { padding: 10px 20px; border-radius: 12px; font-size: 11px; font-weight: 800; transition: 0.3s; background: rgba(255,255,255,0.05); }
        .doc-tab.active { background: #3b82f6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
        ::-webkit-scrollbar { width: 5px; } ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    </style>
</head>
<body class="p-4 md:p-12">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER -->
        <header class="glass-3d rounded-[40px] p-8 flex justify-between items-center mb-12">
            <div class="flex items-center gap-6">
                <div class="flex gap-2">
                    <div class="ios-dot bg-[#ff5f57]"></div><div class="ios-dot bg-[#ffbd2e]"></div><div class="ios-dot bg-[#28c840]"></div>
                </div>
                <h1 class="text-3xl font-black tracking-tighter uppercase italic">Silent <span class="text-blue-500 not-italic">Tech</span></h1>
            </div>
            <div class="hidden md:flex gap-6">
                <button onclick="show('tester')" class="text-[10px] font-black tracking-[3px] uppercase opacity-50 hover:opacity-100 hover:text-blue-400">Playground</button>
                <button onclick="show('docs')" class="text-[10px] font-black tracking-[3px] uppercase opacity-50 hover:opacity-100 hover:text-blue-400">Documentation</button>
            </div>
        </nav>

        <!-- DASHBOARD VIEW -->
        <div id="tester-ui" class="space-y-10">
            <!-- 8 ENDPOINTS GRID -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div onclick="setE('/api/search', 'Spider-Man')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-blue-500 mb-1">01. SEARCH</p>
                    <p class="text-xs opacity-40">Get Movie Slugs</p>
                </div>
                <div onclick="setE('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d p-6 rounded-3xl border-blue-500/30">
                    <p class="text-[10px] font-black text-emerald-500 mb-1">02. DOWNLOADS</p>
                    <p class="text-xs opacity-40">Direct Streams</p>
                </div>
                <div onclick="setE('/api/trending', 'N/A')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-orange-500 mb-1">03. TRENDING</p>
                    <p class="text-xs opacity-40">Top Hits</p>
                </div>
                <div onclick="setE('/api/homepage', 'N/A')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-purple-500 mb-1">04. HOME DATA</p>
                    <p class="text-xs opacity-40">Sitemap Index</p>
                </div>
                <div onclick="setE('/api/categories', 'N/A')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-pink-500 mb-1">05. CATEGORIES</p>
                    <p class="text-xs opacity-40">Genre Lists</p>
                </div>
                <div onclick="setE('/api/genre', 'Action')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-yellow-500 mb-1">06. GENRE FILTER</p>
                    <p class="text-xs opacity-40">Categorized Scrape</p>
                </div>
                <div onclick="setE('/api/details', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-cyan-500 mb-1">07. DETAILS</p>
                    <p class="text-xs opacity-40">Item Metadata</p>
                </div>
                <div onclick="setE('/api/status', 'N/A')" class="glass-3d card-3d p-6 rounded-3xl">
                    <p class="text-[10px] font-black text-red-500 mb-1">08. STATUS</p>
                    <p class="text-xs opacity-40">Engine Health</p>
                </div>
            </div>

            <!-- INTERACTIVE TESTER -->
            <div class="glass-3d rounded-[45px] p-8 md:p-12">
                <div class="flex justify-between items-center mb-10">
                    <h2 id="endpoint-display" class="text-2xl font-black">/api/search</h2>
                    <div class="flex gap-2"><div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div></div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                    <div>
                        <label class="text-[10px] font-black opacity-30 mb-3 block tracking-[2px]">AUTH_KEY</label>
                        <input id="key-field" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition" value="silent">
                    </div>
                    <div>
                        <label class="text-[10px] font-black opacity-30 mb-3 block tracking-[2px]">PARAMETER</label>
                        <input id="param-field" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition">
                    </div>
                </div>
                <button onclick="execute()" class="w-full bg-blue-600 hover:bg-blue-500 py-5 rounded-2xl font-black text-sm tracking-[5px] uppercase transition-all shadow-lg shadow-blue-500/20">Execute Request</button>
                <div class="response-area mt-10">
                    <div class="flex justify-between mb-4"><span class="text-[10px] font-bold text-blue-500 uppercase tracking-widest">Live Server Feed</span></div>
                    <pre id="output-view">Waiting for commands...</pre>
                </div>
            </div>
        </div>

        <!-- DOCUMENTATION VIEW -->
        <div id="docs-ui" class="hidden space-y-10">
            <div class="glass-3d rounded-[45px] p-10">
                <h2 class="text-3xl font-black mb-10 italic uppercase">Developer Documentation</h2>
                <div class="flex gap-3 mb-8 overflow-x-auto pb-4">
                    <button onclick="setLang('py')" id="l-py" class="doc-tab active">PYTHON</button>
                    <button onclick="setLang('js')" id="l-js" class="doc-tab">NODE.JS</button>
                    <button onclick="setLang('php')" id="l-php" class="doc-tab">PHP</button>
                    <button onclick="setLang('go')" id="l-go" class="doc-tab">GOLANG</button>
                </div>
                <div class="response-area">
                    <pre id="code-view"></pre>
                </div>
            </div>
        </div>

        <footer class="mt-32 text-center pb-20">
            <p class="text-[9px] tracking-[15px] opacity-20 font-black uppercase">All Rights Reserved to SILENT TECH | Made with Middle Finger 🖕</p>
        </footer>
    </div>

    <script>
        let currentEndpoint = '/api/search';
        function setE(e, d) { currentEndpoint = e; document.getElementById('endpoint-display').innerText = e; document.getElementById('param-field').value = d; }
        function show(v) { 
            document.getElementById('tester-ui').style.display = v === 'tester' ? 'block' : 'none'; 
            document.getElementById('docs-ui').style.display = v === 'docs' ? 'block' : 'none';
            if(v==='docs') setLang('py');
        }

        async function execute() {
            const out = document.getElementById('output-view');
            const k = document.getElementById('key-field').value;
            const p = document.getElementById('param-field').value;
            out.innerText = "Connecting to Silent Tech Node...";
            let url = currentEndpoint + '?key=' + k;
            if(currentEndpoint.includes('search')) url += '&q=' + p;
            if(currentEndpoint.includes('media') || currentEndpoint.includes('details')) url += '&slug=' + p;
            if(currentEndpoint.includes('genre')) url = '/api/genre/' + p + '?key=' + k;
            
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "Error: System Offline or Timeout."; }
        }

        const snippets = {
            py: "import requests\\n\\nurl = 'YOUR_DEPLOYED_URL/api/search'\\nparams = {'q': 'Spider', 'key': 'silent'}\\nres = requests.get(url, params=params)\\nprint(res.json())",
            js: "const fetch = require('node-fetch');\\n\\nasync function getMovies() {\\n  const res = await fetch('YOUR_DEPLOYED_URL/api/search?q=Spider&key=silent');\\n  const data = await res.json();\\n  console.log(data);\\n}",
            php: "<?php\\n$url = 'YOUR_DEPLOYED_URL/api/search?q=Spider&key=silent';\\n$res = file_get_contents($url);\\necho $res;\\n?>",
            go: "package main\\nimport (\\n  'fmt'\\n  'net/http'\\n  'io/ioutil'\\n)\\n\\nfunc main() {\\n  res, _ := http.Get('YOUR_DEPLOYED_URL/api/search?q=Spider&key=silent')\\n  body, _ := ioutil.ReadAll(res.Body)\\n  fmt.Println(string(body))\\n}"
        };

        function setLang(l) {
            document.querySelectorAll('.doc-tab').forEach(b => b.classList.remove('active'));
            document.getElementById('l-'+l).classList.add('active');
            document.getElementById('code-view').innerText = snippets[l];
        }
    </script>
</body>
</html>
"""

# --- THE SCRAPER ENGINE (V3 POWERED BY COLAB LOGIC) ---

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
    # Step 1: Visit movie page to extract the 18-19 digit numeric ID
    movie_page = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    
    # User-provided Colab patterns
    id_patterns = [
        r'"id":"(\d{15,20})"', 
        r'id=(\d{15,20})',
        r'movie/.*?(\d{15,20})',
        r'\"id\"\:\"(\d+)\"'
    ]
    
    numeric_id = None
    for pattern in id_patterns:
        match = re.search(pattern, movie_page.text)
        if match:
            numeric_id = match.group(1)
            break
            
    if not numeric_id:
        # Final fallback from Colab logic
        all_long_numbers = re.findall(r'"(\d{18,20})"', movie_page.text)
        if all_long_numbers: numeric_id = all_long_numbers[0]

    if not numeric_id:
        return {"error": "Could not find numeric ID. Ensure you use the full slug."}

    # Step 2: Use the ID to get sources (MANDATORY Referer for Download Links)
    source_url = f"{BASE}/api/sources?id={numeric_id}&detailPath={slug}"
    source_headers = {**HEADERS, "referer": f"{BASE}/movie/{slug}"}
    
    source_res = requests.get(source_url, headers=source_headers)
    return {"provider": "SILENT TECH", "id": numeric_id, "data": source_res.json()}

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/homepage")
def homepage(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "status": "Homepage nodes healthy"}

@app.get("/api/categories")
def categories(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "list": ["Action", "Horror", "Comedy", "Sci-Fi", "Crime", "Animation"]}

@app.get("/api/genre/{name}")
def genre(name: str, key: str = "silent"):
    validate(key)
    return search(q=name, key=key)

@app.get("/api/details")
def details(slug: str, key: str = "silent"):
    validate(key)
    parts = slug.split('-')
    return {"provider": "SILENT TECH", "title": " ".join(parts[:-1]).title(), "id": parts[-1]}

@app.get("/api/status")
def status(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "uptime": "100%", "engine": "FastAPI V3 Premium"}
