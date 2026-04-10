# 🎬 MovieBox REST API — Vercel Deployment

Unofficial REST API wrapping [moviebox-api](https://github.com/Simatwa/moviebox-api), deployable on Vercel in one command.

## 🚀 Deploy

```bash
# 1. Clone / copy this project
git clone <your-repo>
cd moviebox-vercel-api

# 2. Install Vercel CLI
npm i -g vercel

# 3. Deploy
vercel deploy --prod
```

That's it. Your API will be live at `https://<your-project>.vercel.app`.

---

## 📖 Interactive Docs

| URL | Description |
|-----|-------------|
| `/api/docs` | Swagger UI |
| `/api/redoc` | ReDoc |
| `/api/openapi.json` | OpenAPI schema |

---

## 📡 Endpoints

### Info

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api` | API info & endpoint map |
| GET | `/api/mirrors` | Available MovieBox mirror hosts |

### Discovery

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/homepage` | Homepage content (featured, new releases, banners) |
| GET | `/api/trending` | Currently trending titles |
| GET | `/api/popular-searches` | Popular search terms |

### Search & Content

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/search` | Search movies & series |
| GET | `/api/details` | Full details by ID |
| GET | `/api/movie` | Movie stream URL + subtitles |
| GET | `/api/series` | Episode stream URL + subtitles |
| GET | `/api/series/seasons` | Season list for a series |
| GET | `/api/series/episodes` | Episode list for a season |

---

## 🔍 Query Parameters

### `/api/search`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | ✅ | Search query |
| `type` | string | ❌ | `movie` or `series` |
| `year` | int | ❌ | Release year filter |
| `page` | int | ❌ | Page number (default: 1) |

**Example:**
```
GET /api/search?q=Avatar&type=movie&year=2009
```

---

### `/api/movie`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | ✅ | Movie title |
| `quality` | string | ❌ | `best` `1080p` `720p` `480p` `360p` `worst` |
| `year` | int | ❌ | Release year |
| `language` | string | ❌ | Subtitle language (default: `English`) |
| `no_caption` | bool | ❌ | Skip subtitle fetch |

**Example:**
```
GET /api/movie?q=Avatar&quality=1080p&year=2009
```

**Response:**
```json
{
  "title": "Avatar",
  "year": 2009,
  "id": "abc123",
  "quality": "1080p",
  "sources": { "url": "https://...", "quality": "1080p" },
  "subtitles": { "url": "https://...", "language": "English" }
}
```

---

### `/api/series`

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `q` | string | ✅ | Series title |
| `season` | int | ✅ | Season number |
| `episode` | int | ✅ | Episode number |
| `quality` | string | ❌ | Video quality |
| `language` | string | ❌ | Subtitle language |
| `no_caption` | bool | ❌ | Skip subtitles |

**Example:**
```
GET /api/series?q=Breaking+Bad&season=1&episode=1&quality=1080p
```

---

### `/api/series/episodes`

| Param | Required | Description |
|-------|----------|-------------|
| `id` | ✅ | Series ID (from search) |
| `season` | ✅ | Season number |

**Example:**
```
GET /api/series/episodes?id=abc123&season=2
```

---

### `/api/trending`

| Param | Required | Description |
|-------|----------|-------------|
| `type` | ❌ | `movie` or `series` |

---

### `/api/details`

| Param | Required | Description |
|-------|----------|-------------|
| `id` | ✅ | Movie or series ID |

---

## ⚙️ Environment Variables

Set these in Vercel project settings → Environment Variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `MOVIEBOX_API_HOST` | V1 mirror host | `moviebox.ph` |
| `MOVIEBOX_API_HOST_V2` | V2 mirror host | `h5-api.aoneroom.com` |

To find working mirrors:
```
GET /api/mirrors
```

---

## 🛠️ Local Development

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload --port 8000
```

Then open: http://localhost:8000/api/docs

---

## 📦 Usage Examples

### Curl

```bash
# Search
curl "https://your-api.vercel.app/api/search?q=Inception"

# Get movie stream URL
curl "https://your-api.vercel.app/api/movie?q=Inception&quality=1080p"

# Get series episode
curl "https://your-api.vercel.app/api/series?q=Breaking+Bad&season=1&episode=1"

# Homepage content
curl "https://your-api.vercel.app/api/homepage"

# Trending
curl "https://your-api.vercel.app/api/trending?type=movie"
```

### JavaScript / Fetch

```js
const BASE = "https://your-api.vercel.app";

// Search
const res = await fetch(`${BASE}/api/search?q=Avatar`);
const data = await res.json();
console.log(data.results);

// Get stream URL
const movie = await fetch(`${BASE}/api/movie?q=Avatar&quality=1080p`);
const { sources } = await movie.json();
videoElement.src = sources.url;
```

### Python

```python
import httpx

BASE = "https://your-api.vercel.app"

r = httpx.get(f"{BASE}/api/movie", params={"q": "Avatar", "quality": "720p"})
data = r.json()
print(data["sources"])
```

---

## ⚠️ Disclaimer

All content is sourced from MovieBox. This wrapper is unofficial and for educational purposes.
"All videos and pictures on MovieBox are from the Internet, and their copyrights belong to the original creators."
