
# FastAPI version: Accepts a URL, runs the crew, and returns the output as JSON
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from crew import run_crew_for_url
from tasks import AnalysisOutput

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "output", "report.txt")

class UrlRequest(BaseModel):
	url: str


def format_analysis_output(analysis: AnalysisOutput) -> str:
	"""Format the structured AnalysisOutput into a well-formatted text report."""
	report_lines = []
	
	# Core Claims
	report_lines.append("CORE CLAIMS")
	report_lines.append("=" * 60)
	for i, claim in enumerate(analysis.core_claims, 1):
		report_lines.append(f"{i}. {claim}")
	report_lines.append("")
	
	# Tone Analysis
	report_lines.append("LANGUAGE & TONE ANALYSIS")
	report_lines.append("=" * 60)
	report_lines.append(analysis.tone_analysis)
	report_lines.append("")
	
	# Red Flags
	report_lines.append("POTENTIAL RED FLAGS")
	report_lines.append("=" * 60)
	if analysis.red_flags:
		for i, flag in enumerate(analysis.red_flags, 1):
			report_lines.append(f"{i}. {flag}")
	else:
		report_lines.append("None identified")
	report_lines.append("")
	
	# Verification Questions
	report_lines.append("VERIFICATION QUESTIONS")
	report_lines.append("=" * 60)
	for i, question in enumerate(analysis.verification_questions, 1):
		report_lines.append(f"{i}. {question}")
	report_lines.append("")
	
	# Named Entities (BONUS)
	if analysis.named_entities:
		report_lines.append("NAMED ENTITY RECOGNITION (BONUS)")
		report_lines.append("=" * 60)
		for entity_type, entities in analysis.named_entities.items():
			if entities:
				report_lines.append(f"{entity_type.upper()}:")
				for entity in entities:
					report_lines.append(f"  - {entity}")
		report_lines.append("")
	
	# Opposing Viewpoint (BONUS)
	if analysis.opposing_viewpoint:
		report_lines.append("OPPOSING VIEWPOINT (BONUS)")
		report_lines.append("=" * 60)
		report_lines.append(analysis.opposing_viewpoint)
		report_lines.append("")
	
	return "\n".join(report_lines)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=PlainTextResponse)
async def analyze_url(data: UrlRequest):
	os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
	
	try:
		# Run the crew and get structured output
		result = run_crew_for_url(data.url)
		
		# Extract the AnalysisOutput from the last task
		if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
			analysis_output = result.tasks_output[-1].pydantic
			if isinstance(analysis_output, AnalysisOutput):
				formatted_report = format_analysis_output(analysis_output)
				
				# Save to file for compatibility
				with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
					f.write(formatted_report)
				
				return formatted_report
		
		return "No output generated."
	
	except Exception as e:
		error_msg = str(e)
		
		# Handle specific API errors
		if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
			return (
				"⚠️ API RATE LIMIT EXCEEDED\n\n"
				"The Google Gemini API has reached its rate limit.\n"
				"Free tier limit: 5 requests per minute for gemini-2.5-flash\n\n"
				"Please wait 30-60 seconds and try again.\n\n"
				"Tip: Consider using a different model or upgrading your API plan.\n"
				"Monitor usage at: https://ai.dev/usage?tab=rate-limit"
			)
		elif "503" in error_msg or "UNAVAILABLE" in error_msg:
			return (
				"⚠️ API SERVICE UNAVAILABLE\n\n"
				"The Google Gemini API is currently overloaded or unavailable.\n\n"
				"Please try again in a few moments."
			)
		elif "401" in error_msg or "403" in error_msg:
			return (
				"⚠️ AUTHENTICATION ERROR\n\n"
				"Invalid or missing API key.\n\n"
				"Please check your GOOGLE_API_KEY in the .env file."
			)
		else:
			# Generic error handler
			return (
				"⚠️ ERROR\n\n"
				f"An error occurred while analyzing the article:\n\n{error_msg}\n\n"
				"Please try again or check the server logs for details."
			)
