from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Only v1 is exposed as a Python API — v2 is CLI-only
from moviebox_api.v1 import MovieAuto
from moviebox_api.v1.cli import Downloader

app = FastAPI(
    title="MovieBox API",
    description="Unofficial REST API for MovieBox — search, stream, and download movies & TV series",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# ROOT
# ──────────────────────────────────────────────

@app.get("/api", tags=["Info"])
async def root():
    return {
        "name": "MovieBox API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "search":           "GET /api/search?q=Avatar",
            "movie":            "GET /api/movie?q=Avatar&quality=1080p",
            "movie_auto":       "GET /api/movie/auto?q=Avatar",
            "series":           "GET /api/series?q=Breaking+Bad&season=1&episode=1",
            "series_seasons":   "GET /api/series/seasons?id=ITEM_ID",
            "series_episodes":  "GET /api/series/episodes?id=ITEM_ID&season=1",
            "homepage":         "GET /api/homepage",
            "trending":         "GET /api/trending",
            "popular_searches": "GET /api/popular-searches",
            "details":          "GET /api/details?id=ITEM_ID",
            "mirrors":          "GET /api/mirrors",
        },
    }


# ──────────────────────────────────────────────
# HELPER — safely serialize any object
# ──────────────────────────────────────────────

def _s(obj):
    if obj is None:
        return None
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, list):
        return [_s(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _s(v) for k, v in obj.items()}
    if hasattr(obj, "__dict__"):
        return {k: _s(v) for k, v in vars(obj).items() if not k.startswith("_")}
    return obj


def _downloader(**kwargs):
    return Downloader(
        caption_language=kwargs.get("language", "English"),
        quality=kwargs.get("quality", "best"),
        download_dir="/tmp",
        autofill=True,
    )


# ──────────────────────────────────────────────
# SEARCH
# ──────────────────────────────────────────────

@app.get("/api/search", tags=["Search"])
async def search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Filter: movie | series"),
    year: Optional[int] = Query(None, description="Release year"),
    page: int = Query(1, ge=1),
):
    """Search for movies and TV series."""
    try:
        d = _downloader()
        results = await d.search(q, page=page)
        items = results if isinstance(results, list) else getattr(results, "results", [_s(results)])

        if type:
            items = [i for i in items if str(getattr(i, "type", "")).lower() == type.lower()]
        if year:
            items = [i for i in items if getattr(i, "year", None) == year]

        return {"query": q, "page": page, "count": len(items), "results": [_s(i) for i in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# HOMEPAGE
# ──────────────────────────────────────────────

@app.get("/api/homepage", tags=["Discovery"])
async def homepage():
    """Homepage featured content."""
    try:
        d = _downloader()
        data = await d.homepage_content()
        return _s(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# TRENDING
# ──────────────────────────────────────────────

@app.get("/api/trending", tags=["Discovery"])
async def trending(
    type: Optional[str] = Query(None, description="movie | series"),
):
    """Currently trending titles."""
    try:
        d = _downloader()
        data = await d.trending()
        items = data if isinstance(data, list) else getattr(data, "results", [_s(data)])
        if type:
            items = [i for i in items if str(getattr(i, "type", "")).lower() == type.lower()]
        return {"count": len(items), "results": [_s(i) for i in items]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# POPULAR SEARCHES
# ──────────────────────────────────────────────

@app.get("/api/popular-searches", tags=["Discovery"])
async def popular_searches():
    """Popular search terms."""
    try:
        d = _downloader()
        data = await d.popular_searches()
        return {"results": _s(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# DETAILS
# ──────────────────────────────────────────────

@app.get("/api/details", tags=["Content"])
async def details(
    id: str = Query(..., description="Movie or series ID"),
):
    """Full metadata for a movie or series by ID."""
    try:
        d = _downloader()
        data = await d.item_details(id)
        return _s(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# MOVIE — stream sources
# ──────────────────────────────────────────────

@app.get("/api/movie", tags=["Content"])
async def movie_sources(
    q: str = Query(..., description="Movie title"),
    quality: str = Query("best", description="best | 1080p | 720p | 480p | 360p | worst"),
    year: Optional[int] = Query(None),
    language: str = Query("English", description="Subtitle language"),
    no_caption: bool = Query(False),
):
    """Get stream URL and subtitle URL for a movie."""
    try:
        d = _downloader(quality=quality, language=language)
        movie_file, subtitle_files = await d.download_movie(
            q, year=year, no_download=True
        )
        return {
            "title": getattr(movie_file, "title", q),
            "year": getattr(movie_file, "year", year),
            "quality": quality,
            "stream_url": getattr(movie_file, "url", None) or getattr(movie_file, "stream_url", None),
            "size": getattr(movie_file, "size", None),
            "subtitles": None if no_caption else [_s(s) for s in (subtitle_files or [])],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# MOVIE — auto (highest quality, first result)
# ──────────────────────────────────────────────

@app.get("/api/movie/auto", tags=["Content"])
async def movie_auto(
    q: str = Query(..., description="Movie title"),
    quality: str = Query("best"),
    language: str = Query("English"),
):
    """Auto-select best match and return stream + subtitle URLs."""
    try:
        auto = MovieAuto(
            caption_language=language,
            quality=quality,
            download_dir="/tmp",
        )
        movie_file, subtitle_file = await auto.run(q, no_download=True)
        return {
            "title": getattr(movie_file, "title", q),
            "stream_url": getattr(movie_file, "url", None) or getattr(movie_file, "stream_url", None),
            "subtitle_url": getattr(subtitle_file, "url", None) if subtitle_file else None,
            "quality": quality,
            "language": language,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# TV SERIES — stream sources
# ──────────────────────────────────────────────

@app.get("/api/series", tags=["Content"])
async def series_sources(
    q: str = Query(..., description="Series title"),
    season: int = Query(..., ge=1),
    episode: int = Query(..., ge=1),
    quality: str = Query("best"),
    language: str = Query("English"),
    no_caption: bool = Query(False),
):
    """Get stream URL and subtitle URL for a TV series episode."""
    try:
        d = _downloader(quality=quality, language=language)
        episodes_map = await d.download_tv_series(
            q, season=season, episode=episode, limit=1, no_download=True
        )
        ep_key = f"S{season:02d}E{episode:02d}"
        ep_data = episodes_map.get(ep_key) or (list(episodes_map.values())[0] if episodes_map else None)

        if not ep_data:
            raise HTTPException(status_code=404, detail=f"Episode {ep_key} not found for '{q}'")

        video, subs = ep_data if isinstance(ep_data, (tuple, list)) else (ep_data, [])
        return {
            "title": getattr(video, "title", q),
            "season": season,
            "episode": episode,
            "quality": quality,
            "stream_url": getattr(video, "url", None) or getattr(video, "stream_url", None),
            "size": getattr(video, "size", None),
            "subtitles": None if no_caption else [_s(s) for s in (subs or [])],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# SERIES — seasons
# ──────────────────────────────────────────────

@app.get("/api/series/seasons", tags=["Content"])
async def series_seasons(
    id: str = Query(..., description="Series ID (from /api/search)"),
):
    """List all seasons for a TV series."""
    try:
        d = _downloader()
        data = await d.seasons(id)
        return {"id": id, "seasons": _s(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# SERIES — episodes
# ──────────────────────────────────────────────

@app.get("/api/series/episodes", tags=["Content"])
async def series_episodes(
    id: str = Query(..., description="Series ID"),
    season: int = Query(..., ge=1),
):
    """List all episodes in a season."""
    try:
        d = _downloader()
        data = await d.episodes(id, season=season)
        return {"id": id, "season": season, "episodes": _s(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# MIRRORS
# ──────────────────────────────────────────────

@app.get("/api/mirrors", tags=["Info"])
async def mirrors():
    """Discover available MovieBox mirror hosts."""
    try:
        d = _downloader()
        data = await d.mirror_hosts()
        return {"mirrors": _s(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
