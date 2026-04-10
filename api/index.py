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
@app.get("/api/hot-series")
@app.get("/api/home")
def placeholder(key: str = Depends(check_key)):
    return {"success": True, "results": []}

@app.get("/api/status")
def status(key: str = Depends(check_key)):
    return {"status": "Premium", "online": True}

# MINIMAL GLASSMORPHISM DASHBOARD
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT TECH</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap');
        body { background: #0a0a0a; font-family: 'Inter', system_ui, sans-serif; perspective: 1200px; }
        .glass { background: rgba(255,255,255,0.06); backdrop-filter: blur(24px); border: 1px solid rgba(255,255,255,0.12); }
        .card-hover:hover { transform: translateY(-3px); box-shadow: 0 15px 30px -10px rgb(0 212 255 / 0.25); }
        .accent { color: #00d4ff; }
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
            <a onclick="showSection('tester')" class="hover:text-[#00d4ff]">TESTER</a>
            <a onclick="showSection('docs')" class="hover:text-[#00d4ff]">DOCS</a>
            <a onclick="showSection('status')" class="hover:text-[#00d4ff]">STATUS</a>
        </div>
    </div>

    <div class="max-w-screen-2xl mx-auto px-8 py-12">
        <!-- API TESTER -->
        <div id="tester-section">
            <h2 class="text-5xl font-semibold tracking-tighter mb-2">API TESTER</h2>
            <p class="text-white/60 mb-10">Live scraper • Zero latency • 100% working streams</p>
            
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12" id="endpoint-grid"></div>

            <div class="glass rounded-3xl p-8 mb-8">
                <input id="request-url" type="text" value="/api/search?q=ironman&key=silent" 
                       class="w-full bg-transparent text-lg font-mono focus:outline-none">
                <button onclick="sendRequest()" 
                        class="mt-6 w-full py-4 bg-[#00d4ff] text-black font-semibold rounded-3xl hover:bg-[#00b8e0]">SEND REQUEST →</button>
            </div>

            <div class="glass rounded-3xl p-8">
                <div id="json-output" class="json-viewer bg-black/70 p-8 rounded-2xl text-[#00d4ff] overflow-auto max-h-[420px]"></div>
            </div>
        </div>

        <!-- Coming Soon -->
        <div class="mt-20 border-t border-white/10 pt-12">
            <h3 class="text-xl mb-8 flex items-center gap-3"><span class="text-[#00d4ff]">🚀</span> COMING SOON TO SILENT TECH</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass rounded-3xl p-6">Seedance 2.0 Video Generation</div>
                <div class="glass rounded-3xl p-6">4K HDR Streaming Engine</div>
                <div class="glass rounded-3xl p-6">AI Subtitle Translator v2</div>
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
                card.className = 'glass rounded-3xl p-8 text-center cursor-pointer card-hover';
                card.innerHTML = `
                    <div class="text-[#00d4ff] text-3xl font-semibold">${ep.name}</div>
                    <div class="font-mono text-sm text-white/70 mt-3">${ep.path}</div>
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
                    document.getElementById('json-output').innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                })
                .catch(() => {
                    document.getElementById('json-output').innerHTML = `<div class="text-red-400">ACCESS DENIED BY SILENT TECH 🖕</div>`;
                });
        }

        function showSection(s) {
            document.getElementById('tester-section').scrollIntoView({ behavior: 'smooth' });
        }

        window.onload = populateEndpoints;
    </script>
</body>
</html>"""

@app.get("/")
async def dashboard():
    return HTMLResponse(content=DASHBOARD_HTML)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
