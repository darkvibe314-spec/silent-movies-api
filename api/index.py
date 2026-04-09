from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import requests
import re
import json

app = FastAPI()

# --- THE ENGINE CONFIG ---
BASE = "https://cinverse.name.ng"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "referer": BASE
}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- THE 3D PREMIUM UI ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT PRO API | 3D PLATFORM</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #020203; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; perspective: 1000px; }
        .glass-3d { 
            background: rgba(255, 255, 255, 0.03); 
            backdrop-filter: blur(30px); 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            transform: translateZ(20px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        .card-3d:hover {
            transform: translateY(-5px) rotateX(2deg) rotateY(-2deg);
            border-color: #3b82f6;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        }
        .response-box { 
            background: #000; border: 1px solid #2d3748; border-radius: 15px; 
            padding: 20px; font-family: 'Courier New', monospace; font-size: 11px; 
            color: #60a5fa; overflow: auto; max-height: 400px; 
            scrollbar-width: thin; scrollbar-color: #3b82f6 #000;
        }
        pre { white-space: pre-wrap; word-wrap: break-word; }
        .ios-dot { width: 11px; height: 11px; border-radius: 50%; }
        .premium-btn { 
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .premium-btn:active { transform: scale(0.95) translateZ(0); }
    </style>
</head>
<body class="p-4 md:p-12 overflow-x-hidden">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER 3D -->
        <nav class="glass-3d rounded-[40px] p-8 flex justify-between items-center mb-16">
            <div class="flex items-center gap-6">
                <div class="flex gap-2">
                    <div class="ios-dot bg-[#ff5f57]"></div><div class="ios-dot bg-[#ffbd2e]"></div><div class="ios-dot bg-[#28c840]"></div>
                </div>
                <h1 class="text-3xl font-black tracking-tighter">SILENT <span class="text-blue-500 font-normal italic">PLATFORM</span></h1>
            </div>
            <div class="flex gap-6">
                <button onclick="setView('tester')" class="text-xs font-bold uppercase tracking-widest opacity-60 hover:opacity-100 hover:text-blue-400">Tester</button>
                <button onclick="setView('docs')" class="text-xs font-bold uppercase tracking-widest opacity-60 hover:opacity-100 hover:text-blue-400">Docs</button>
            </div>
        </nav>

        <!-- TESTER VIEW -->
        <div id="tester-view" class="space-y-12">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-6">
                <div onclick="setE('/api/search', 'Spider-Man')" class="glass-3d card-3d rounded-3xl p-6 transition-all cursor-pointer">
                    <div class="text-xs font-bold text-blue-500 mb-1">01. Search</div>
                    <div class="text-[10px] opacity-40">Keywords & Slugs</div>
                </div>
                <div onclick="setE('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="glass-3d card-3d rounded-3xl p-6 transition-all cursor-pointer">
                    <div class="text-xs font-bold text-emerald-500 mb-1">02. Media Links</div>
                    <div class="text-[10px] opacity-40">Direct Downloads</div>
                </div>
                <div onclick="setE('/api/trending', 'N/A')" class="glass-3d card-3d rounded-3xl p-6 transition-all cursor-pointer">
                    <div class="text-xs font-bold text-orange-500 mb-1">03. Trending</div>
                    <div class="text-[10px] opacity-40">Current Releases</div>
                </div>
                <div onclick="setE('/api/homepage', 'N/A')" class="glass-3d card-3d rounded-3xl p-6 transition-all cursor-pointer">
                    <div class="text-xs font-bold text-purple-500 mb-1">04. Homepage</div>
                    <div class="text-[10px] opacity-40">Sitemap Data</div>
                </div>
            </div>

            <div class="glass-3d rounded-[45px] p-10">
                <div class="flex justify-between items-center mb-10">
                    <h2 id="curr-endpoint" class="text-2xl font-black">/api/search</h2>
                    <span class="text-[10px] bg-blue-600 px-4 py-1 rounded-full font-bold uppercase tracking-widest">GET REQUEST</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
                    <div>
                        <label class="text-[10px] font-black opacity-30 mb-4 block tracking-widest">API_KEY</label>
                        <input id="k-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition" value="silent">
                    </div>
                    <div>
                        <label class="text-[10px] font-black opacity-30 mb-4 block tracking-widest">PARAM_VALUE</label>
                        <input id="p-in" class="w-full bg-black/40 border border-white/10 rounded-2xl p-4 outline-none focus:border-blue-500 transition" value="">
                    </div>
                </div>
                <button onclick="run()" class="premium-btn w-full py-5 rounded-2xl font-black text-sm tracking-[5px] uppercase">Execute Command</button>
                <div class="response-box mt-10">
                    <div class="flex justify-between mb-4"><span class="text-[10px] font-bold text-blue-400">SILENT_SERVER_FEED</span><span id="stat" class="text-[10px]">IDLE</span></div>
                    <pre id="out">SYSTEM STANDBY...</pre>
                </div>
            </div>
        </div>

        <!-- DOCS VIEW -->
        <div id="docs-view" class="hidden space-y-10">
            <div class="glass-3d rounded-[45px] p-10">
                <h2 class="text-3xl font-black mb-10 tracking-tighter">Documentation Portal</h2>
                <div class="flex gap-3 mb-10 overflow-x-auto pb-4">
                    <button onclick="setL('py')" id="t-py" class="text-[10px] font-black px-6 py-3 rounded-xl transition bg-blue-600">PYTHON</button>
                    <button onclick="setL('js')" id="t-js" class="text-[10px] font-black px-6 py-3 rounded-xl transition bg-white/5">NODE.JS</button>
                    <button onclick="setL('php')" id="t-php" class="text-[10px] font-black px-6 py-3 rounded-xl transition bg-white/5">PHP</button>
                    <button onclick="setL('go')" id="t-go" class="text-[10px] font-black px-6 py-3 rounded-xl transition bg-white/5">GOLANG</button>
                </div>
                <div class="response-box">
                    <pre id="code-v"></pre>
                </div>
            </div>
        </div>

        <footer class="mt-32 text-center pb-20">
            <div class="h-[1px] bg-white/5 mb-10"></div>
            <p class="text-[10px] tracking-[15px] opacity-30 font-black uppercase">ALL RIGHTS RESERVED TO SILENT TECH | MADE WITH MIDDLE FINGER 🖕</p>
        </footer>
    </div>

    <script>
        let cur = '/api/search';
        function setE(e, d) { cur = e; document.getElementById('curr-endpoint').innerText = e; document.getElementById('p-in').value = d; }
        function setView(v) { 
            document.getElementById('tester-view').style.display = v === 'tester' ? 'block' : 'none'; 
            document.getElementById('docs-view').style.display = v === 'docs' ? 'block' : 'none';
            if(v==='docs') setL('py');
        }

        async function run() {
            const out = document.getElementById('out');
            const k = document.getElementById('k-in').value;
            const p = document.getElementById('p-in').value;
            out.innerText = "Connecting to Silent Tech Node...";
            let url = cur + '?key=' + k;
            if(cur.includes('search')) url += '&q=' + p;
            if(cur.includes('media') || cur.includes('details')) url += '&slug=' + p;
            
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "SERVER_TIMEOUT_ERROR"; }
        }

        const snips = {
            py: "import requests\\n\\nurl = 'https://YOUR_DOMAIN/api/search'\\nparams = {'q': 'Batman', 'key': 'silent'}\\nres = requests.get(url, params=params)\\nprint(res.json())",
            js: "const fetch = require('node-fetch');\\n\\nasync function getMovies() {\\n  const res = await fetch('https://YOUR_DOMAIN/api/search?q=Batman&key=silent');\\n  const data = await res.json();\\n  console.log(data);\\n}",
            php: "<?php\\n$url = 'https://YOUR_DOMAIN/api/search?q=Batman&key=silent';\\n$res = file_get_contents($url);\\necho $res;\\n?>",
            go: "package main\\nimport (\\n  'fmt'\\n  'net/http'\\n  'io/ioutil'\\n)\\n\\nfunc main() {\\n  res, _ := http.Get('https://YOUR_DOMAIN/api/search?q=Batman&key=silent')\\n  body, _ := ioutil.ReadAll(res.Body)\\n  fmt.Println(string(body))\\n}"
        };

        function setL(l) {
            document.querySelectorAll('#docs-view button').forEach(b => b.classList.replace('bg-blue-600', 'bg-white/5'));
            document.getElementById('t-'+l).classList.replace('bg-white/5', 'bg-blue-600');
            document.getElementById('code-v').innerText = snips[l];
        }
    </script>
</body>
</html>
"""

# --- THE SCRAPER ENGINE (V2 FIXED) ---

@app.get("/", response_class=HTMLResponse)
def root(): return HTML_UI

@app.get("/api/search")
def search(q: str, key: str = "silent"):
    validate(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}

@app.get("/api/media")
def media(slug: str, key: str = "silent"):
    validate(key)
    # Step 1: Visit the movie page to scrape the secret numeric ID
    movie_page = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    
    # Aggressive ID search (multiple patterns for Vercel stability)
    num_id = re.search(r'"id":"(\d{15,20})"', movie_page.text)
    if not num_id:
        num_id = re.search(r'\"id\"\:\"(\d+)\"', movie_page.text)
    
    if not num_id:
        return {"error": "Media metadata not found. Use full slug.", "tip": "Search first to get the correct slug."}

    # Step 2: Call the real source API with the found ID
    source_url = f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}"
    # This header is MANDATORY for the download links to appear
    src_headers = {**HEADERS, "referer": f"{BASE}/movie/{slug}", "accept": "*/*"}
    
    src_res = requests.get(source_url, headers=src_headers)
    return {"provider": "SILENT TECH", "slug": slug, "media_data": src_res.json()}

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/homepage")
def homepage(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "status": "Ready", "data_origin": "Silent Node v1"}

@app.get("/api/categories")
def categories(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "list": ["Action", "Horror", "Comedy", "Sci-Fi", "Crime", "Animation"]}

@app.get("/api/details")
def details(slug: str, key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "item": slug, "details": "Syncing metadata..."}

@app.get("/api/status")
def status(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "system": "Premium", "latency": "Low"}
