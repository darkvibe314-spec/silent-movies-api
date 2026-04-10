from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import asyncio

from moviebox_api.v2 import MovieBoxV2
from moviebox_api.v1 import MovieAuto

app = FastAPI(
    title="MovieBox API",
    description="Unofficial REST API for MovieBox - search, stream, and download movies & TV series",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client():
    return MovieBoxV2()


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
            "search":    "GET /api/search",
            "movie":     "GET /api/movie",
            "series":    "GET /api/series",
            "homepage":  "GET /api/homepage",
            "trending":  "GET /api/trending",
            "details":   "GET /api/details",
            "mirrors":   "GET /api/mirrors",
            "popular_searches": "GET /api/popular-searches",
        },
    }


# ──────────────────────────────────────────────
# SEARCH
# ──────────────────────────────────────────────

@app.get("/api/search", tags=["Search"])
async def search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Filter by type: movie | series"),
    year: Optional[int] = Query(None, description="Filter by release year"),
    page: int = Query(1, ge=1, description="Page number"),
):
    """Search for movies and TV series by title."""
    try:
        client = get_client()
        results = await client.search(q, page=page)

        items = results if isinstance(results, list) else getattr(results, "results", results)

        if type:
            items = [i for i in items if getattr(i, "type", "").lower() == type.lower()]
        if year:
            items = [i for i in items if getattr(i, "year", None) == year]

        return {
            "query": q,
            "page": page,
            "count": len(items),
            "results": [_serialize(i) for i in items],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# HOMEPAGE
# ──────────────────────────────────────────────

@app.get("/api/homepage", tags=["Discovery"])
async def homepage():
    """Get homepage content — featured, new releases, banners, etc."""
    try:
        client = get_client()
        data = await client.homepage()
        return _serialize(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# TRENDING
# ──────────────────────────────────────────────

@app.get("/api/trending", tags=["Discovery"])
async def trending(
    type: Optional[str] = Query(None, description="Filter by type: movie | series"),
):
    """Get currently trending movies and TV series."""
    try:
        client = get_client()
        data = await client.trending()
        items = data if isinstance(data, list) else getattr(data, "results", [data])

        if type:
            items = [i for i in items if getattr(i, "type", "").lower() == type.lower()]

        return {
            "count": len(items),
            "results": [_serialize(i) for i in items],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# POPULAR SEARCHES
# ──────────────────────────────────────────────

@app.get("/api/popular-searches", tags=["Discovery"])
async def popular_searches():
    """Get current popular search terms."""
    try:
        client = get_client()
        data = await client.popular_searches()
        return {"results": _serialize(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# ITEM DETAILS
# ──────────────────────────────────────────────

@app.get("/api/details", tags=["Content"])
async def details(
    id: str = Query(..., description="Movie or series ID"),
):
    """Get full details for a specific movie or TV series by its ID."""
    try:
        client = get_client()
        data = await client.details(id)
        return _serialize(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# MOVIE — SOURCES & STREAM URL
# ──────────────────────────────────────────────

@app.get("/api/movie", tags=["Content"])
async def movie_sources(
    q: str = Query(..., description="Movie title"),
    quality: str = Query("best", description="Quality: best | 1080p | 720p | 480p | 360p | worst"),
    year: Optional[int] = Query(None, description="Release year to narrow search"),
    language: str = Query("English", description="Subtitle language"),
    no_caption: bool = Query(False, description="Skip subtitle fetch"),
):
    """
    Search for a movie and return its stream URL(s) and subtitle URL.
    Use the returned `stream_url` to play or proxy the video.
    """
    try:
        client = get_client()

        # Search
        results = await client.search(q)
        items = results if isinstance(results, list) else getattr(results, "results", [])
        movies = [i for i in items if getattr(i, "type", "").lower() in ("movie", "")]
        if year:
            movies = [i for i in movies if getattr(i, "year", None) == year] or movies

        if not movies:
            raise HTTPException(status_code=404, detail=f"No movies found for '{q}'")

        item = movies[0]
        item_id = getattr(item, "id", None) or getattr(item, "item_id", None)

        # Get sources
        sources = await client.movie_sources(item_id, quality=quality)

        result = {
            "title": getattr(item, "title", q),
            "year": getattr(item, "year", None),
            "id": item_id,
            "quality": quality,
            "sources": _serialize(sources),
        }

        if not no_caption:
            try:
                subs = await client.movie_subtitles(item_id, language=language)
                result["subtitles"] = _serialize(subs)
            except Exception:
                result["subtitles"] = None

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# TV SERIES — SOURCES & STREAM URL
# ──────────────────────────────────────────────

@app.get("/api/series", tags=["Content"])
async def series_sources(
    q: str = Query(..., description="Series title"),
    season: int = Query(..., ge=1, description="Season number"),
    episode: int = Query(..., ge=1, description="Episode number"),
    quality: str = Query("best", description="Quality: best | 1080p | 720p | 480p | 360p | worst"),
    language: str = Query("English", description="Subtitle language"),
    no_caption: bool = Query(False, description="Skip subtitle fetch"),
):
    """
    Search for a TV series episode and return its stream URL(s) and subtitle URL.
    """
    try:
        client = get_client()

        results = await client.search(q)
        items = results if isinstance(results, list) else getattr(results, "results", [])
        series = [i for i in items if getattr(i, "type", "").lower() in ("series", "tv", "tvshow")]

        if not series:
            raise HTTPException(status_code=404, detail=f"No TV series found for '{q}'")

        item = series[0]
        item_id = getattr(item, "id", None) or getattr(item, "item_id", None)

        sources = await client.episode_sources(item_id, season=season, episode=episode, quality=quality)

        result = {
            "title": getattr(item, "title", q),
            "id": item_id,
            "season": season,
            "episode": episode,
            "quality": quality,
            "sources": _serialize(sources),
        }

        if not no_caption:
            try:
                subs = await client.episode_subtitles(
                    item_id, season=season, episode=episode, language=language
                )
                result["subtitles"] = _serialize(subs)
            except Exception:
                result["subtitles"] = None

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# SERIES — EPISODE LIST
# ──────────────────────────────────────────────

@app.get("/api/series/episodes", tags=["Content"])
async def series_episodes(
    id: str = Query(..., description="Series ID"),
    season: int = Query(..., ge=1, description="Season number"),
):
    """List all episodes for a given season."""
    try:
        client = get_client()
        data = await client.episodes(id, season=season)
        return {
            "id": id,
            "season": season,
            "episodes": _serialize(data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# SERIES — SEASON LIST
# ──────────────────────────────────────────────

@app.get("/api/series/seasons", tags=["Content"])
async def series_seasons(
    id: str = Query(..., description="Series ID"),
):
    """List all available seasons for a TV series."""
    try:
        client = get_client()
        data = await client.seasons(id)
        return {
            "id": id,
            "seasons": _serialize(data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# MIRRORS
# ──────────────────────────────────────────────

@app.get("/api/mirrors", tags=["Info"])
async def mirrors():
    """Discover available MovieBox mirror hosts."""
    try:
        client = get_client()
        data = await client.mirror_hosts()
        return {"mirrors": _serialize(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────────

def _serialize(obj):
    """Recursively convert Pydantic models / dataclasses to dicts."""
    if obj is None:
        return None
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "__dict__"):
        return {k: _serialize(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [_serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj
