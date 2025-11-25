import logging
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from .api.router import router
from .core.config import get_settings

# 1. ADVANCED LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# ---------------------------------------------------------------------------
# 2. ROBUST LOGIC TO LOCATE THE FRONTEND
# ---------------------------------------------------------------------------

# Get the absolute path of the folder where main.py resides (.../app)
current_file_path = Path(__file__).resolve()
app_dir = current_file_path.parent
root_dir = app_dir.parent

logger.info(f"📁 PATH DEBUG: Main.py is at: {current_file_path}")
logger.info(f"📁 PATH DEBUG: Root dir detected as: {root_dir}")

# Search strategy:
# 1. Look in /home/site/wwwroot/frontend (Confirmed by your 'find' command)
# 2. Look in /home/site/wwwroot/app/static (Legacy fallback)
potential_paths = [
    root_dir / "frontend",
    app_dir / "static",
    root_dir / "static"
]

frontend_dir = None

for path in potential_paths:
    if path.exists() and (path / "index.html").exists():
        frontend_dir = path
        logger.info(f"✅ FRONTEND FOUND AT: {frontend_dir}")
        break
    else:
        logger.warning(f"❌ Frontend not found at: {path}")

# ---------------------------------------------------------------------------
# 3. STATIC FILES MOUNT
# ---------------------------------------------------------------------------

if frontend_dir:
    # Mount static assets (js, css, img)
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    
    # Serve index.html at root with nuclear Anti-Cache
    @app.get("/", response_class=HTMLResponse)
    async def serve_frontend(response: Response):
        index_file = frontend_dir / "index.html"
        
        # Headers to prevent ANY browser caching during development
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        
        if index_file.exists():
            content = index_file.read_text(encoding="utf-8")
            return HTMLResponse(content=content, headers=response.headers)
        return HTMLResponse(content="Error: index.html missing despite check", status_code=500)

else:
    logger.error("🔥 CRITICAL: Frontend directory could not be located anywhere!")
    @app.get("/", response_class=HTMLResponse)
    async def root():
        return HTMLResponse(
            content="<h1>Backend Running</h1><p>Error: Frontend files not found on server.</p>",
            status_code=404
        )

# ---------------------------------------------------------------------------
# 4. STARTUP CHECK
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 ETL Assistant Chatbot RESTARTING - NEW CODE LOADED")
    if frontend_dir:
        index_path = frontend_dir / "index.html"
        if index_path.exists():
            # Print the file size: if it doesn't change, the deploy failed
            size = index_path.stat().st_size
            logger.info(f"📄 Index.html detected. Size: {size} bytes")
            # Print the first 50 characters to check if it's the new file
            try:
                content_preview = index_path.read_text(encoding="utf-8")[:50]
                logger.info(f"📄 Content Preview: {content_preview}...")
            except Exception as e:
                logger.error(f"Could not read index preview: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)