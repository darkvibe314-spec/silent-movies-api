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

# PREMIUM SAAS DASHBOARD HTML
DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILENT TECH</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap');
        body { background: #0a0a0a; font-family: 'Inter', system_ui, sans-serif; }
        .hero-bg { background: linear-gradient(90deg, #00ff9d10, #000000); }
        .glass { background: rgba(255,255,255,0.08); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); }
        .card-hover:hover { transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgb(0 255 157 / 0.2); }
    </style>
</head>
<body class="text-white">
    <!-- HEADER -->
    <div class="max-w-screen-2xl mx-auto px-8 py-6 flex items-center justify-between">
        <div class="flex items-center gap-x-3">
            <div class="w-9 h-9 bg-[#00ff9d] rounded-2xl flex items-center justify-center text-black font-bold text-2xl">S</div>
            <h1 class="text-3xl font-semibold tracking-tighter" style="font-family: 'Space Grotesk', sans-serif;">SILENT TECH</h1>
        </div>
        <div class="flex items-center gap-x-8 text-sm font-medium">
            <a onclick="showSection('tester')" class="hover:text-[#00ff9d]">TESTER</a>
            <a onclick="showSection('docs')" class="hover:text-[#00ff9d]">DOCS</a>
            <a onclick="showSection('status')" class="hover:text-[#00ff9d]">STATUS</a>
        </div>
    </div>

    <!-- HERO -->
    <div class="hero-bg py-20 text-center">
        <div class="max-w-3xl mx-auto px-6">
            <h1 class="text-6xl font-semibold tracking-tighter leading-none mb-6">The Ultimate<br>Movie Streaming API</h1>
            <p class="text-xl text-white/70 mb-10">Access millions of movies and TV series with a single API. Stream, download, and integrate movie data into your applications with ease.</p>
            <div class="flex justify-center gap-4">
                <button onclick="showSection('tester')" class="px-8 py-4 bg-[#00ff9d] text-black font-semibold rounded-3xl text-lg flex items-center gap-2 hover:scale-105 transition">Get Started Free →</button>
                <button onclick="showSection('docs')" class="px-8 py-4 border border-white/30 rounded-3xl text-lg flex items-center gap-2 hover:bg-white/10">Read Documentation</button>
            </div>
        </div>
    </div>

    <!-- STATS -->
    <div class="max-w-screen-2xl mx-auto px-8 py-12 grid grid-cols-2 md:grid-cols-4 gap-6">
        <div class="glass rounded-3xl p-8 text-center">
            <div class="text-5xl font-semibold text-[#00ff9d]">∞</div>
            <div class="text-sm uppercase tracking-widest mt-2">Movies &amp; Series</div>
        </div>
        <div class="glass rounded-3xl p-8 text-center">
            <div class="text-5xl font-semibold text-[#00ff9d]">100%</div>
            <div class="text-sm uppercase tracking-widest mt-2">Uptime</div>
        </div>
        <div class="glass rounded-3xl p-8 text-center">
            <div class="text-5xl font-semibold text-[#00ff9d]">0ms</div>
            <div class="text-sm uppercase tracking-widest mt-2">Latency</div>
        </div>
        <div class="glass rounded-3xl p-8 text-center">
            <div class="text-5xl font-semibold text-[#00ff9d]">🖕</div>
            <div class="text-sm uppercase tracking-widest mt-2">Built Different</div>
        </div>
    </div>

    <!-- FEATURES -->
    <div class="max-w-screen-2xl mx-auto px-8 py-16">
        <h2 class="text-4xl font-semibold text-center mb-12">Powerful Features</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" id="feature-grid"></div>
    </div>

    <!-- API TESTER -->
    <div id="tester-section" class="max-w-screen-2xl mx-auto px-8 py-16 border-t border-white/10">
        <h2 class="text-5xl font-semibold tracking-tighter text-center mb-4">API TESTER</h2>
        <p class="text-center text-white/60 mb-12">Live scraper • Zero latency • 100% working streams</p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12" id="endpoint-grid"></div>
        <div class="glass rounded-3xl p-8">
            <input id="request-url" class="w-full bg-transparent text-lg font-mono" value="/api/search?q=ironman&key=silent">
            <button onclick="sendRequest()" class="mt-6 w-full py-4 bg-[#00ff9d] text-black font-semibold rounded-3xl">SEND REQUEST →</button>
        </div>
        <div class="glass rounded-3xl p-8 mt-6">
            <div id="json-output" class="json-viewer bg-black/70 p-8 rounded-2xl text-emerald-300 overflow-auto max-h-[420px]"></div>
        </div>
    </div>

    <!-- COMING SOON + FOOTER -->
    <div class="max-w-screen-2xl mx-auto px-8 py-16 border-t border-white/10 text-center">
        <h3 class="text-xl mb-8 flex items-center justify-center gap-3"><span class="text-[#00ff9d]">🚀</span> COMING SOON TO SILENT TECH</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl mx-auto">
            <div class="glass rounded-3xl p-6">Seedance 2.0 Video Generation</div>
            <div class="glass rounded-3xl p-6">4K HDR Streaming Engine</div>
            <div class="glass rounded-3xl p-6">AI Subtitle Translator v2</div>
        </div>
        <div class="mt-16 text-xs text-white/40">
            ALL RIGHTS RESERVED TO SILENT TECH | MADE WITH MIDDLE FINGER 🖕
        </div>
    </div>

    <script>
        const endpoints = [
            {name:"SEARCH", path:"/api/search", param:"q=ironman"},
            {name:"MEDIA", path:"/api/media", param:"id=6268300615831947768"},
            {name:"TRENDING", path:"/api/trending", param:""},
            {name:"HOT SERIES", path:"/api/hot-series", param:""},
            {name:"HOME", path:"/api/home", param:""}
        ];

        function populateEndpoints() {
            const grid = document.getElementById('endpoint-grid');
            grid.innerHTML = '';
            endpoints.forEach(ep => {
                const card = document.createElement('div');
                card.className = 'glass rounded-3xl p-8 text-center cursor-pointer card-hover';
                card.innerHTML = `<div class="text-[#00ff9d] text-3xl font-semibold">\( {ep.name}</div><div class="font-mono text-sm mt-2"> \){ep.path}</div>`;
                card.onclick = () => document.getElementById('request-url').value = ep.path + (ep.param ? '?' + ep.param + '&key=silent' : '?key=silent');
                grid.appendChild(card);
            });
        }

        function sendRequest() {
            const url = document.getElementById('request-url').value;
            fetch(url).then(r => r.json()).then(d => {
                document.getElementById('json-output').innerHTML = `<pre>${JSON.stringify(d, null, 2)}</pre>`;
            }).catch(() => document.getElementById('json-output').innerHTML = `<div class="text-red-400">ACCESS DENIED BY SILENT TECH 🖕</div>`);
        }

        function showSection(section) {
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
