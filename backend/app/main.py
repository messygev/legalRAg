from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.health import router as health_router
from app.api.search import router as search_router
from app.api.notices import router as notices_router

app = FastAPI(title="Legal RAG Bescheid-Kompass")
app.include_router(health_router)
app.include_router(search_router)
app.include_router(notices_router)
app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get('/')
def ui() -> FileResponse:
    return FileResponse('app/static/index.html')
