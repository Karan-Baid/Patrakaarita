
# FastAPI version: Accepts a URL, runs the crew, and returns the output as JSON
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from crew import run_crew_for_url

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output", "report.txt")

class UrlRequest(BaseModel):
	url: str



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=PlainTextResponse)
async def analyze_url(data: UrlRequest):
	os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
	run_crew_for_url(data.url)
	if os.path.exists(OUTPUT_PATH):
		with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
			return f.read()
	return "No output generated."
