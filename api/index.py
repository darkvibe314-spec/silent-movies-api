from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(title="SILENT TECH", docs_url=None, redoc_url=None)

BASE_URL = "https://mv.paxsenix.org"
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://mv.paxsenix.org/',
    'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99", "Microsoft Edge Simulate";v="127", "Lemur";v="127"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36'
}

def check_key(key: str = Query(None)):
    if key != "silent":
        raise HTTPException(status_code=401, detail="ACCESS DENIED BY SILENT TECH 🖕")
    return key

# Endpoints
@app.get("/api/search")
def search(q: str = Query(...), key: str = Depends(check_key)):
    try:
        r = requests.get(f"{BASE_URL}/api/search?q={q}", headers=HEADERS, timeout=15)
        return r.json() if r.ok else {"success": False, "results": []}
    except:
        return {"success": False, "results": []}

@app.get("/api/media")
def media(movie_id: str = Query(..., alias="id"), key: str = Depends(check_key)):
    try:
        r = requests.get(f"{BASE_URL}/api/sources/{movie_id}", headers=HEADERS, timeout=15)
        return {"provider": "SILENT TECH", "movie_id": movie_id, "data": r.json() if r.ok else {"error": "Failed"}}
    except:
        return {"error": "Media fetch failed"}

@app.get("/api/trending")
def trending(key: str = Depends(check_key)):
    return {"success": True, "results": []}

@app.get("/api/hot-series")
def hot_series(key: str = Depends(check_key)):
    return {"success": True, "results": []}

@app.get("/api/home")
def home(key: str = Depends(check_key)):
    return {"status": "synced"}

@app.get("/api/status")
def status(key: str = Depends(check_key)):
    return {"status": "Premium", "online": True}

# FULL UPDATED DASHBOARD HTML
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT TECH</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500&display=swap');
        body { background: #020203; font-family: 'Inter', system_ui, sans-serif; perspective: 1200px; }
        .glass { background: rgba(255,255,255,0.06); backdrop-filter: blur(24px); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.4); }
        .card-3d { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .card-3d:hover { transform: translateY(-4px) scale(1.03); box-shadow: 0 35px 60px -15px rgb(0 255 157 / 0.3); }
        .json-viewer { white-space: pre-wrap !important; word-break: break-all; font-family: ui-monospace; font-size: 13px; line-height: 1.5; }
    </style>
</head>
<body class="min-h-screen text-white">
    <div class="max-w-screen-2xl mx-auto px-8 py-6 flex items-center justify-between border-b border-white/10">
        <div class="flex items-center gap-x-3">
            <div class="flex gap-x-2">
                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <h1 class="text-3xl font-semibold tracking-tighter" style="font-family: 'Space Grotesk', sans-serif;">SILENT TECH</h1>
        </div>
        <div class="flex items-center gap-x-8 text-sm font-medium">
            <a onclick="showSection('tester')" class="hover:text-[#00ff9d]">TESTER</a>
            <a onclick="showSection('docs')" class="hover:text-[#00ff9d]">DOCS</a>
            <a onclick="showSection('status')" class="hover:text-[#00ff9d]">STATUS</a>
        </div>
    </div>

    <div class="max-w-screen-2xl mx-auto px-8 py-10">
        <!-- TESTER -->
        <div id="tester-section">
            <h2 class="text-5xl font-semibold tracking-tighter mb-2">API TESTER</h2>
            <p class="text-white/60 mb-8">Live scraper • Zero latency • 100% working streams</p>
            
            <!-- CLEAN GRID -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10" id="endpoint-grid"></div>

            <div class="glass rounded-3xl p-8 mb-8">
                <input id="request-url" type="text" value="/api/search?q=ironman&key=silent" 
                       class="w-full bg-transparent text-lg font-mono focus:outline-none">
                <button onclick="sendRequest()" 
                        class="mt-6 px-10 py-4 bg-[#00ff9d] text-black font-semibold rounded-3xl w-full">SEND REQUEST →</button>
            </div>

            <div class="glass rounded-3xl p-8">
                <div id="json-output" class="json-viewer bg-black/60 p-6 rounded-2xl text-emerald-300 min-h-[300px]"></div>
            </div>
        </div>

        <!-- DOCS & STATUS (same as before) -->
        <div id="docs-section" class="hidden">... (documentation tabs) ...</div>
        <div id="status-section" class="hidden">... (status) ...</div>

        <!-- COMING SOON -->
        <div class="mt-16 border-t border-white/10 pt-10">
            <h3 class="text-xl font-semibold mb-6 flex items-center gap-3">
                <span class="text-[#00ff9d]">🚀</span> COMING SOON TO SILENT TECH
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass rounded-3xl p-6">• Seedance 2.0 Video Generation</div>
                <div class="glass rounded-3xl p-6">• 4K Ultra HDR Streaming</div>
                <div class="glass rounded-3xl p-6">• AI Subtitle Translator v2</div>
            </div>
        </div>
    </div>

    <div class="text-center py-8 text-xs text-white/40 border-t border-white/10">
        ALL RIGHTS RESERVED TO SILENT TECH | MADE WITH MIDDLE FINGER 🖕
    </div>

    <script>
        const endpoints = [
            {name: "SEARCH", path: "/api/search", param: "q=ironman"},
            {name: "MEDIA", path: "/api/media", param: "id=6268300615831947768"},
            {name: "TRENDING", path: "/api/trending", param: ""},
            {name: "HOT SERIES", path: "/api/hot-series", param: ""},
            {name: "HOME", path: "/api/home", param: ""}
        ];

        function populateEndpoints() {
            const grid = document.getElementById('endpoint-grid');
            grid.innerHTML = '';
            endpoints.forEach(ep => {
                const card = document.createElement('div');
                card.className = 'glass rounded-3xl p-6 cursor-pointer text-center card-3d';
                card.innerHTML = `
                    <div class="text-[#00ff9d] text-2xl font-semibold">${ep.name}</div>
                    <div class="font-mono text-sm text-white/70 mt-1">${ep.path}</div>
                `;
                card.onclick = () => {
                    document.getElementById('request-url').value = ep.path + (ep.param ? '?' + ep.param + '&key=silent' : '?key=silent');
                };
                grid.appendChild(card);
            });
        }

        function sendRequest() {
            const url = document.getElementById('request-url').value;
            fetch(url)
                .then(r => r.json())
                .then(data => {
                    document.getElementById('json-output').innerHTML = `<pre class="json-viewer">${JSON.stringify(data, null, 2)}</pre>`;
                })
                .catch(() => {
                    document.getElementById('json-output').innerHTML = `<div class="text-red-400">ACCESS DENIED BY SILENT TECH 🖕</div>`;
                });
        }

        function showSection(s) {
            document.querySelectorAll('#tester-section, #docs-section, #status-section').forEach(el => el.classList.add('hidden'));
            document.getElementById(s + '-section').classList.remove('hidden');
        }

        window.onload = () => {
            populateEndpoints();
            showSection('tester');
        };
    </script>
</body>
</html>"""

@app.get("/")
async def dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
