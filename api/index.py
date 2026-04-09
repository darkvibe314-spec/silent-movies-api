from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import requests
import re
import json

app = FastAPI()

# --- CONFIGURATION ---
BASE = "https://cinverse.name.ng"
HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# --- THE UI (EMBEDDED FOR ZERO ERRORS) ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT MOVIE API | DASHBOARD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&display=swap" rel="stylesheet">
    <style>
        body { background: #020202; color: #fff; font-family: 'Space Grotesk', sans-serif; overflow-x: hidden; }
        .glass { background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(25px); border: 1px solid rgba(255,255,255,0.05); }
        .ios-dot { width: 12px; height: 12px; border-radius: 50%; }
        ::-webkit-scrollbar { width: 5px; } ::-webkit-scrollbar-thumb { background: #3b82f6; border-radius: 10px; }
    </style>
</head>
<body class="p-4 md:p-10">
    <div class="max-w-7xl mx-auto">
        <!-- HEADER -->
        <nav class="glass rounded-[35px] p-6 flex justify-between items-center mb-10 shadow-2xl">
            <div class="flex items-center gap-6">
                <div class="flex gap-2">
                    <div class="ios-dot bg-[#ff5f57]"></div><div class="ios-dot bg-[#ffbd2e]"></div><div class="ios-dot bg-[#28c840]"></div>
                </div>
                <h1 class="text-2xl font-black tracking-tighter text-blue-500">SILENT <span class="text-white">API</span></h1>
            </div>
            <div class="hidden md:block text-[9px] tracking-[6px] uppercase opacity-40">SYSTEM STATUS: ONLINE | SECURED BY SILENT TECH</div>
        </nav>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <!-- DOCS SIDEBAR -->
            <div class="lg:col-span-4 space-y-6">
                <div class="glass rounded-[30px] p-8">
                    <h2 class="text-blue-500 font-bold text-lg mb-6 tracking-widest">DOCUMENTATION</h2>
                    <div class="space-y-4">
                        <div>
                            <p class="text-[10px] uppercase opacity-40 mb-2">Python Snippet</p>
                            <pre class="bg-black/60 p-4 rounded-2xl text-[10px] text-green-400 overflow-x-auto">res = requests.get(url + "/api/v1/trending?key=silent")</pre>
                        </div>
                        <div>
                            <p class="text-[10px] uppercase opacity-40 mb-2">Node.js Snippet</p>
                            <pre class="bg-black/60 p-4 rounded-2xl text-[10px] text-blue-300 overflow-x-auto">const data = await fetch("/api/v1/search?q=Batman&key=silent")</pre>
                        </div>
                    </div>
                </div>
                <div class="glass rounded-[30px] p-8">
                    <h2 class="text-blue-500 font-bold text-lg mb-4 tracking-widest">CATEGORIES (8+)</h2>
                    <div class="grid grid-cols-2 gap-2 text-[9px] font-bold uppercase opacity-50">
                        <div class="p-3 border border-white/5 rounded-xl">Trending</div><div class="p-3 border border-white/5 rounded-xl">Download</div>
                        <div class="p-3 border border-white/5 rounded-xl">Streaming</div><div class="p-3 border border-white/5 rounded-xl">Action</div>
                        <div class="p-3 border border-white/5 rounded-xl">Adventure</div><div class="p-3 border border-white/5 rounded-xl">Horror</div>
                        <div class="p-3 border border-white/5 rounded-xl">Sci-Fi</div><div class="p-3 border border-white/5 rounded-xl">Crime</div>
                    </div>
                </div>
            </div>

            <!-- INTERACTIVE TESTER -->
            <div class="lg:col-span-8 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <button onclick="runTest('/api/v1/trending')" class="glass p-8 rounded-[30px] text-left hover:bg-white/5 transition-all group">
                        <h3 class="font-bold text-xl group-hover:text-blue-500 transition-colors">Get Trending</h3>
                        <p class="text-xs opacity-40">Fetch top 15 movie releases</p>
                    </button>
                    <button onclick="runTest('/api/v1/search?q=Spider')" class="glass p-8 rounded-[30px] text-left hover:bg-white/5 transition-all group">
                        <h3 class="font-bold text-xl group-hover:text-blue-500 transition-colors">Search Engine</h3>
                        <p class="text-xs opacity-40">Query: Spider-Man (Auto-filled)</p>
                    </button>
                </div>

                <!-- LIVE JSON VIEWER -->
                <div class="glass rounded-[35px] p-8 min-h-[500px] relative">
                    <div class="flex justify-between items-center mb-6">
                        <span class="text-[10px] font-mono text-blue-500 tracking-[3px]">LIVE_SERVER_FEED</span>
                        <div class="flex gap-2"><div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse shadow-[0_0_10px_#3b82f6]"></div></div>
                    </div>
                    <pre id="output" class="text-[11px] font-mono leading-relaxed text-blue-100/70 whitespace-pre-wrap">READY FOR COMMANDS... CLICK A TEST ENDPOINT ABOVE.</pre>
                </div>
            </div>
        </div>

        <footer class="mt-20 text-center pb-20">
            <p class="text-[10px] tracking-[15px] uppercase opacity-20 font-bold">ALL RIGHTS RESERVED TO SILENT TECH | MADE WITH MIDDLE FINGER 🖕</p>
        </footer>
    </div>

    <script>
        async function runTest(path) {
            const out = document.getElementById('output');
            out.innerText = "REQUEST SENT TO SILENT TECH CLUSTER...";
            try {
                const res = await fetch(`${path}&key=silent`);
                const data = await res.json();
                out.innerText = JSON.stringify(data, null, 2);
            } catch(e) { out.innerText = "CRITICAL ERROR: API OFFLINE."; }
        }
    </script>
</body>
</html>
"""

# --- BACKEND LOGIC ---
def validate(key: str):
    if key != "silent":
        raise HTTPException(status_code=401, detail="INVALID KEY - SILENT TECH 🖕")

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_CONTENT

@app.get("/api/v1/trending")
def trending(key: str = "silent"):
    validate(key)
    res = requests.get(BASE, headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"slug": s, "title": s.replace('-', ' ').title()} for s in slugs[:15]]}

@app.get("/api/v1/search")
def search(q: str, key: str = "silent"):
    validate(key)
    res = requests.get(f"{BASE}/search?q={q}", headers=HEADERS)
    slugs = re.findall(r'href="/movie/([^" \>]+)"', res.text)
    return {"provider": "SILENT TECH", "results": [{"title": s.replace('-', ' ').title(), "slug": s} for s in list(set(slugs))]}

@app.get("/api/v1/movie")
def movie(slug: str, key: str = "silent"):
    validate(key)
    p = requests.get(f"{BASE}/movie/{slug}", headers=HEADERS)
    num_id = re.search(r'"id":"(\d{15,20})"', p.text)
    if not num_id: return {"error": "Movie not found"}
    src = requests.get(f"{BASE}/api/sources?id={num_id.group(1)}&detailPath={slug}", headers=HEADERS).json()
    return {"provider": "SILENT TECH", "slug": slug, "id": num_id.group(1), "media": src}

@app.get("/api/v1/categories")
def cats(key: str = "silent"):
    validate(key)
    return {
        "provider": "SILENT TECH",
        "categories": ["Trending", "Streaming", "Download", "Action", "Adventure", "Horror", "Comedy", "Sci-Fi"]
    }
