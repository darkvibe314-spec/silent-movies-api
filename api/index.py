from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import requests
import re

app = FastAPI()

# --- THE ENGINE ---
BASE = "https://cinverse.name.ng"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")

# --- THE FRONTEND (Pro Dashboard + Multi-Lang Docs) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT API | PRO HUB</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { background: #050506; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .card { background: #0f1115; border: 1px solid #1f2937; border-radius: 1.2rem; transition: all 0.3s ease; cursor: pointer; }
        .card:hover { border-color: #3b82f6; background: #161a20; }
        .input-field { background: #08090b; border: 1px solid #2d3748; border-radius: 12px; padding: 12px; color: #fff; width: 100%; outline: none; }
        .response-box { background: #000; border: 1px solid #2d3748; border-radius: 15px; padding: 20px; font-family: monospace; font-size: 11px; color: #60a5fa; min-height: 250px; }
        .tab-btn { padding: 8px 16px; border-radius: 8px; font-size: 11px; font-weight: bold; transition: 0.2s; }
        .tab-active { background: #3b82f6; color: white; }
    </style>
</head>
<body class="p-4 md:p-10">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER -->
        <nav class="glass rounded-[30px] p-6 flex justify-between items-center mb-10">
            <div class="flex items-center gap-4">
                <h1 class="text-2xl font-black tracking-tighter">SILENT <span class="text-blue-500 italic">PRO</span></h1>
            </div>
            <div class="flex gap-4">
                <button onclick="toggleView('tester')" class="text-xs font-bold uppercase tracking-widest opacity-60 hover:opacity-100">Tester</button>
                <button onclick="toggleView('docs')" class="text-xs font-bold uppercase tracking-widest opacity-60 hover:opacity-100">Documentation</button>
            </div>
        </nav>

        <!-- TESTER VIEW -->
        <div id="tester-view" class="space-y-10">
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
                <div onclick="setE('/api/search', 'Spider-Man')" class="card p-5">
                    <div class="text-xs font-bold text-blue-500 mb-1">01. Search</div>
                    <div class="text-[10px] opacity-40">Keyword matching</div>
                </div>
                <div onclick="setE('/api/media', 'spider-man-homecoming-ylSxcJY0uNa')" class="card p-5">
                    <div class="text-xs font-bold text-emerald-500 mb-1">02. Media</div>
                    <div class="text-[10px] opacity-40">Streams & Downloads</div>
                </div>
                <div onclick="setE('/api/trending', 'N/A')" class="card p-5">
                    <div class="text-xs font-bold text-orange-500 mb-1">03. Trending</div>
                    <div class="text-[10px] opacity-40">Global releases</div>
                </div>
                <div onclick="setE('/api/homepage', 'N/A')" class="card p-5">
                    <div class="text-xs font-bold text-purple-500 mb-1">04. Homepage</div>
                    <div class="text-[10px] opacity-40">Featured content</div>
                </div>
                <div onclick="setE('/api/categories', 'N/A')" class="card p-5">
                    <div class="text-xs font-bold text-pink-500 mb-1">05. Categories</div>
                    <div class="text-[10px] opacity-40">Genre lists</div>
                </div>
                <div onclick="setE('/api/genre', 'Action')" class="card p-5">
                    <div class="text-xs font-bold text-yellow-500 mb-1">06. Genre Filter</div>
                    <div class="text-[10px] opacity-40">Targeted results</div>
                </div>
                <div onclick="setE('/api/details', 'spider-man-homecoming-ylSxcJY0uNa')" class="card p-5">
                    <div class="text-xs font-bold text-cyan-500 mb-1">07. Details</div>
                    <div class="text-[10px] opacity-40">Item metadata</div>
                </div>
                <div onclick="setE('/api/status', 'N/A')" class="card p-5">
                    <div class="text-xs font-bold text-red-500 mb-1">08. Status</div>
                    <div class="text-[10px] opacity-40">Health check</div>
                </div>
            </div>

            <div class="glass rounded-[30px] p-8">
                <div class="flex justify-between items-center mb-6">
                    <h2 id="current-endpoint" class="text-xl font-bold">Select an endpoint</h2>
                    <span class="text-[10px] bg-blue-600 px-3 py-1 rounded-full font-bold uppercase">GET</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div>
                        <label class="text-[10px] font-bold opacity-30 mb-2 block">API KEY</label>
                        <input id="key-in" class="input-field" value="silent">
                    </div>
                    <div>
                        <label class="text-[10px] font-bold opacity-30 mb-2 block uppercase">PARAMETER (ID/Slug/Query)</label>
                        <input id="param-in" class="input-field" value="">
                    </div>
                </div>
                <button onclick="run()" class="w-full bg-blue-600 py-4 rounded-xl font-bold active:scale-95 transition">EXECUTE REQUEST</button>
                <pre id="out" class="response-box mt-6 overflow-auto">Waiting for execution...</pre>
            </div>
        </div>

        <!-- DOCS VIEW -->
        <div id="docs-view" class="hidden space-y-8">
            <div class="glass rounded-[30px] p-8">
                <h2 class="text-2xl font-black mb-6">API Documentation</h2>
                <div class="flex gap-2 mb-8 overflow-x-auto pb-2">
                    <button onclick="lang('py')" id="b-py" class="tab-btn tab-active">PYTHON</button>
                    <button onclick="lang('js')" id="b-js" class="tab-btn bg-white/5">NODE.JS</button>
                    <button onclick="lang('php')" id="b-php" class="tab-btn bg-white/5">PHP</button>
                    <button onclick="lang('go')" id="b-go" class="tab-btn bg-white/5">GOLANG</button>
                    <button onclick="lang('curl')" id="b-curl" class="tab-btn bg-white/5">CURL</button>
                </div>
                <pre id="code-box" class="response-box text-blue-200">Select a language...</pre>
            </div>
        </div>

        <footer class="mt-20 text-center pb-20 opacity-20 text-[9px] tracking-[10px] font-black uppercase">
            ALL RIGHTS RESERVED TO SILENT TECH | MADE WITH MIDDLE FINGER 🖕
        </footer>
    </div>

    <script>
        let curE = '';
        function setE(path, def) {
            curE = path;
            document.getElementById('current-endpoint').innerText = path;
            document.getElementById('param-in').value = def;
        }

        async function run() {
            const out = document.getElementById('out');
            const key = document.getElementById('key-in').value;
            const param = document.getElementById('param-in').value;
            out.innerText = "Processing...";
            let url = curE + '?key=' + key;
            if(curE.includes('search')) url += '&q=' + param;
            if(curE.includes('media') || curE.includes('details')) url += '&slug=' + param;
            if(curE.includes('genre')) url = curE + '/' + param + '?key=' + key;
            
            try {
                const res = await fetch(url);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "Error fetching data."; }
        }

        function toggleView(v) {
            document.getElementById('tester-view').style.display = v === 'tester' ? 'block' : 'none';
            document.getElementById('docs-view').style.display = v === 'docs' ? 'block' : 'none';
            if(v === 'docs') lang('py');
        }

        const snippets = {
            py: "import requests\\n\\nurl = 'YOUR_URL/api/search'\\nparams = {'q': 'Spider', 'key': 'silent'}\\nresponse = requests.get(url, params=params)\\nprint(response.json())",
            js: "const axios = require('axios');\\n\\naxios.get('YOUR_URL/api/search', {\\n  params: { q: 'Spider', key: 'silent' }\\n}).then(res => console.log(res.data));",
            php: "<?php\\n$q = 'Spider';\\n$key = 'silent';\\n$url = 'YOUR_URL/api/search?q='.$q.'&key='.$key;\\n$resp = file_get_contents($url);\\necho $resp;\\n?>",
            go: "package main\\nimport (\\n  'fmt'\\n  'net/http'\\n  'io/ioutil'\\n)\\n\\nfunc main() {\\n  resp, _ := http.Get('YOUR_URL/api/search?q=Spider&key=silent')\\n  body, _ := ioutil.ReadAll(resp.Body)\\n  fmt.Println(string(body))\\n}",
            curl: "curl -X GET 'YOUR_URL/api/search?q=Spider&key=silent'"
        };

        function lang(l) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('tab-active'));
            document.getElementById('b-'+l).classList.add('tab-active');
            document.getElementById('code-box').innerText = snippets[l];
        }
    </script>
</body>
</html>
"""

# --- BACKEND API (8 ENDPOINTS) ---

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
    p = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    num_id = re.search(r'"id":"(\d{15,20})"', p.text)
    if not num_id: return {"error": "Media not found. Ensure full slug is used."}
    src = requests.get(f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}", headers=HEADERS).json()
    return {"provider": "SILENT TECH", "media": src}

@app.get("/api/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/homepage")
def homepage(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "message": "Homepage data sync complete"}

@app.get("/api/categories")
def categories(key: str = "silent"):
    validate(key)
    return {"provider": "SILENT TECH", "list": ["Action", "Horror", "Comedy", "Sci-Fi", "Crime"]}

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
    return {"provider": "SILENT TECH", "status": "Online", "engine": "FastAPI v2"}
