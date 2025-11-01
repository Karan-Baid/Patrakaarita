# Patrakaarita

Light-weight project that orchestrates two AI agents (researcher + analyst) using `crewai` to fetch and analyze news articles from a URL and produce a text report.



---

## Quick overview

- The orchestration entrypoint is `crew.py`. It creates a `Crew` with two `Agent`s defined in `agents.py` and two `Task`s defined in `tasks.py`.
- The `research_task` extracts the article body from a URL. The `analysis_task` analyzes the extracted text and saves a formatted report to `output/report.txt` (see `tasks.py` `output_file` property).
- LLM configuration happens in `agents.py` via the `llm` variable. The project supports using Google GenAI (Gemini) via `crewai[google-genai]` or `litellm` provider strings.

---

## Requirements

- Linux / macOS (development tested on Linux). Windows should work with path adjustments.
- Python 3.10+ (3.11 recommended). The Google client may warn about older 3.10 support.
- A virtual environment (venv or conda) for isolating dependencies.
- A valid Google GenAI API key if using the `google/...` model provider.

---

## Files of interest

- `crew.py` — small CLI-style entrypoint (may be refactored to expose `kickoff_url()` in some workflows).
- `agents.py` — defines two `Agent` objects (`researcher` and `analyst`) and the `llm` configuration.
- `tasks.py` — defines `research_task` and `analysis_task`. `analysis_task` by default writes `output/report.txt`.
- `tools.py` — helper tools used by tasks/agents (e.g., web fetcher or parsers).
- `requirements.txt` — project requirements (includes `crewai[google-genai]`).
- `output/` — (not committed) folder where `analysis_task` saves `report.txt`.

---

## Setup (recommended)

1. Clone the repo (or ensure you're in the workspace root):

```bash
# If you haven't cloned the repository yet, clone it and `cd` into the project folder:
# Replace `<repo-url>` with your repository URL and `/path/to` with a suitable local path.
git clone <repo-url> /path/to/patrakaarita
cd /path/to/patrakaarita

# If you already have the project locally, just change into its root directory:
cd /path/to/patrakaarita
```

2. Create and activate a virtual environment (venv):

```bash
python -m venv venv
source venv/bin/activate
```

If you prefer conda:

```bash
conda create -n patrakaarita python=3.11 -y
conda activate patrakaarita
```

3. Install dependencies from `requirements.txt`:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Note: `requirements.txt` contains `crewai[google-genai]` which installs the native Google GenAI provider for `crewai`.

4. Set environment variables (Google API key):

```bash
# set this in your shell or in a .env file
export GOOGLE_API_KEY="your-google-api-key"
```

If you use a `.env` file, `agents.py` calls `load_dotenv()` so variables from `.env` will be loaded automatically. The recommended file is `.env` in the project root with a line like:

```
GOOGLE_API_KEY=ya...your_key_here
```

Be careful not to commit `.env` to version control.

---

## Running the CLI (crew.py)

By default `crew.py` may run a sample URL. To run it manually with your own URL, edit `crew.py` to call `kickoff_url(...)` (or pass a different URL if the script accepts it). Example quick run:

```bash
# ensure venv active
source venv/bin/activate
python crew.py
```

Expected behavior:
- The researcher agent fetches and extracts the article text.
- The analyst agent runs analysis and writes a report to `output/report.txt` (see `tasks.py`).
- The script prints the `crew.kickoff()` result to stdout.

---

## Accessing output and how it's printed

- The `analysis_task` in `tasks.py` has the parameter `output_file="output/report.txt"`. When that task completes it will write the formatted report to that relative path.
- If you run the CLI locally you can open the file after the run:

```bash
cat output/report.txt
```

- If you build a frontend (Flask/HTTP), you can read and return the contents of `output/report.txt` to the client. Example flow:
  - Frontend sends POST /analyze with body `{ "url": "https://..." }`.
  - Backend runs `kickoff_url(url)` (synchronously or queued). The `analysis_task` will write `output/report.txt`.
  - Frontend polls or requests `/output` endpoint which returns the contents of `output/report.txt`.

Do we need to set an output path for the new changes?
- No, you don't strictly need to change the output path. The project already uses `output/report.txt` (defined in `tasks.py`). If you prefer a different path or dynamic per-request paths, update the `Task` object's `output_file` argument in `tasks.py` or change the analysis task to accept a runtime output path from `crew.kickoff(inputs={...})` and write to that path.

Examples of dynamic output handling:
- Per-request report file: use a unique filename (timestamp or uuid) and pass its path to the task via `inputs` or modify `tasks.py` to accept `output_file` from context.
- Single shared file: keep `output/report.txt` and always overwrite it — simpler but not concurrent-safe.

---


## Web Frontend (FastAPI)

This project includes a modern FastAPI web frontend:
- `web.py` exposes `/` (a form to submit a URL) and `/analyze` (POST endpoint for analysis).
- `templates/index.html` is a professional HTML page styled with `static/style.css`.
- Users enter a news article URL in the browser, submit, and see the output formatted as in the `.txt` file.

How it works:
1. User enters a URL and clicks Analyze.
2. The browser sends a POST to `/analyze` with the URL.
3. The backend runs the crew, writes the output to `output/report.txt`, and returns the result as plain text.
4. The result is displayed in the browser, preserving section formatting.

To run the web frontend:
```bash
uvicorn web:app --reload
# Then open http://localhost:8000 in your browser
```

If you want per-request output files (not always overwriting `output/report.txt`), see the code comments in `tasks.py` and ask for a dynamic output path implementation.

---

## Troubleshooting

1. ImportError / "Fallback to LiteLLM is not available"
   - Install a provider or the `litellm` package if you want that fallback:

```bash
pip install litellm
```

   - Or install `crewai[google-genai]` (already in `requirements.txt`) to use the native Google provider.

2. Google GenAI 404 model not found
   - The model string in `agents.py` (e.g. `google/gemini-1.0` or `google/gemini-2.5-flash`) must match models available to your Google account.
   - To find available models, use the Google GenAI SDK `ListModels` or refer to your Google Cloud console.
   - Change the `llm` variable in `agents.py` to a model permitted for `generateContent`.

3. `dotenv` not found
   - The correct pip package name is `python-dotenv` (we updated `requirements.txt` accordingly). Install via `pip install python-dotenv`.

4. Python version warnings
   - Some client libraries warn about Python 3.10 deprecation. Move to Python 3.11+ to remain supported.

5. Permission / network errors when fetching articles
   - Some news sites block scraping. Consider using a browser-like fetcher (Selenium/playwright) or a reliable content-extraction service.

---

## Development tips

- Use a unique virtual environment per project.
- Add `output/` to `.gitignore` if you don't want reports checked into Git.
- Pin package versions in `requirements.txt` when making deployments.

---

## Example commands recap

```bash
# setup
cd /home/karan/projects/patrakaarita
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GOOGLE_API_KEY="..."

# run analysis (CLI)
python crew.py


