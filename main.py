from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import scraper
import analyzer

app = FastAPI(title="Sosmed Trend Listening & Analytics", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class AnalyzeRequest(BaseModel):
    keyword: str
    time_range: str = "all"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=b"", media_type="image/x-icon")

@app.get("/sw.js", include_in_schema=False)
async def service_worker():
    return Response(content="", media_type="application/javascript")

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze")
async def analyze_trend(payload: AnalyzeRequest):
    keyword = payload.keyword.strip()
    if not keyword:
        return JSONResponse(status_code=400, content={"error": "Keyword tidak boleh kosong"})
    
    time_range = payload.time_range.strip().lower() if payload.time_range else "all"
    
    # 1. Scraping data publik real-time multi-platform dengan filter waktu
    raw_data = scraper.fetch_all_trend_data(keyword, time_range=time_range)
    
    # 2. Analisis Sentimen, Aspek Produk (ABSA), Crisis Alert, & AI Summary
    results = analyzer.analyze_dataset(keyword, raw_data)
    results["time_range"] = time_range
    
    return JSONResponse(content=results)

if __name__ == "__main__":
    import uvicorn
    print("Starting Sosmed Listening Server on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
