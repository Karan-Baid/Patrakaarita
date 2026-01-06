# Patrakaarita 📰

AI-powered news article analysis using CrewAI multi-agent system with Pydantic structured outputs and Groq LLM integration.

---

## ✨ Features

- **🤖 Multi-Agent Architecture** - Researcher extracts content, Analyst evaluates claims and bias
- **⚡ Blazing Fast** - Powered by Groq (world's fastest LLM inference) 
- **📊 Structured Outputs** - Pydantic models ensure clean, validated results (no LLM "thinking")
- **🌐 Web Interface** - FastAPI endpoint with HTML frontend
- **🛡️ Robust Error Handling** - Graceful handling of API errors and rate limits
- **🔧 Modern Tooling** - UV environment management with pyproject.toml

---

## 🏗️ Architecture

### Agents
- **Web Content Extractor** - Fetches and cleans article content from URLs
- **AI Critical Thinking Partner** - Analyzes claims, tone, biases, and verification questions

### Tech Stack
- **Framework**: CrewAI (multi-agent orchestration)
- **LLM**: Groq (llama-3.3-70b-versatile)
- **Web**: FastAPI + Jinja2 templates
- **Validation**: Pydantic models
- **Tools**: SerperDevTool (web search)
- **Environment**: UV package manager

---

## 📋 Requirements

- **Python 3.10+** (3.11 recommended)
- **UV** package manager ([Install UV](https://github.com/astral-sh/uv))
- **Groq API Key** ([Get Free API Key](https://console.groq.com))
- **Serper API Key** ([Get Free API Key](https://serper.dev))

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Karan-Baid/Patrakaarita.git
cd Patrakaarita
```

### 2. Create Virtual Environment

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install fastapi uvicorn "crewai[google-genai]" langchain-google-genai python-dotenv crewai-tools litellm
```

Or install from pyproject.toml:
```bash
uv pip install -e .
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 5. Run the Application

**Web Interface:**
```bash
uvicorn web:app --reload
```
Then open http://localhost:8000 in your browser.

**CLI Mode:**
```bash
python crew.py
```

---

## 📁 Project Structure

```
patrakaarita/
├── agents.py           # Agent definitions (Researcher, Analyst)
├── tasks.py            # Task definitions + Pydantic models
├── crew.py             # Crew orchestration + CLI entrypoint
├── web.py              # FastAPI web server
├── tools.py            # External tools (SerperDevTool)
├── pyproject.toml      # UV dependencies
├── templates/          # HTML templates
├── static/             # CSS styles
└── output/             # Generated reports (gitignored)
```

---

## 🔧 How It Works

### 1. **Research Task**
- Takes a news article URL as input
- Uses SerperDevTool to fetch article content
- Extracts title, author, date, and main content
- Returns structured `ResearchOutput` Pydantic model

### 2. **Analysis Task**
- Receives article content from Research Task
- Analyzes using Groq LLM (llama-3.3-70b-versatile)
- Generates structured `AnalysisOutput` containing:
  - **Core Claims** (3-5 main factual claims)
  - **Tone Analysis** (neutral, emotional, persuasive, etc.)
  - **Red Flags** (bias indicators, weak reporting)
  - **Verification Questions** (3-4 questions to verify claims)
  - **Named Entities** (people, organizations, locations)
  - **Opposing Viewpoint** (hypothetical counter-perspective)

### 3. **Output Formatting**
- Pydantic models ensure structured, validated data
- Web endpoint formats data into clean text report
- No LLM "thinking" or reasoning text in output

---

## 🎯 Usage

### Web Interface

1. Navigate to http://localhost:8000
2. Enter a news article URL
3. Click "Analyze"
4. View formatted analysis report

### CLI Mode

```bash
python crew.py
```

Edit the `sample_url` in `crew.py` to analyze different articles.

### Programmatic Usage

```python
from crew import run_crew_for_url

result = run_crew_for_url("https://example.com/news-article")
analysis = result.tasks_output[-1].pydantic
print(f"Core Claims: {analysis.core_claims}")
```

---

## ⚙️ Configuration

### Change LLM Model

Edit `agents.py`:

```python
# Current: Groq llama-3.3-70b-versatile
llm = "groq/llama-3.3-70b-versatile"

# Alternative Groq models:
# llm = "groq/llama-3.1-70b-versatile"
# llm = "groq/mixtral-8x7b-32768"

# Google Gemini (if you have API key):
# llm = "google/gemini-1.5-flash"
```

### Rate Limits

| Provider | Model | Free Tier RPM |
|----------|-------|---------------|
| Groq | llama-3.3-70b-versatile | **30 RPM** ✅ |
| Groq | llama-3.1-70b-versatile | 30 RPM |
| Google | gemini-1.5-flash | 15 RPM |
| Google | gemini-2.5-flash | 5 RPM |

---

## 🛠️ Troubleshooting

### Rate Limit Errors
If you hit rate limits, the app will show user-friendly error messages. Wait 30-60 seconds and try again.

### Missing Dependencies
```bash
# Install apscheduler to suppress litellm warnings (optional)
uv pip install apscheduler
```

### API Key Issues
Ensure your `.env` file has valid API keys:
```env
GROQ_API_KEY=gsk_...
SERPER_API_KEY=...
```

### Import Errors
Make sure the virtual environment is activated:
```bash
source .venv/bin/activate
```

---

## 📊 Output Format

```
CORE CLAIMS
============================================================
1. [Factual claim from article]
2. [Factual claim from article]
...

LANGUAGE & TONE ANALYSIS
============================================================
[Tone classification and analysis]

POTENTIAL RED FLAGS
============================================================
1. [Bias indicator or weak reporting sign]
...

VERIFICATION QUESTIONS
============================================================
1. [Question to verify claims]
...

NAMED ENTITY RECOGNITION (BONUS)
============================================================
PEOPLE:
  - [Person name]
ORGANIZATIONS:
  - [Organization name]
...

OPPOSING VIEWPOINT (BONUS)
============================================================
[Hypothetical counter-perspective]
```

---

## 🚦 Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/Karan-Baid/Patrakaarita.git
cd Patrakaarita
uv venv
source .venv/bin/activate
uv pip install -e .

# Run with auto-reload
uvicorn web:app --reload
```

### Run Syntax Checks

```bash
python -m py_compile agents.py tasks.py crew.py web.py
```

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📧 Contact

Created by [Karan Baid](https://github.com/Karan-Baid)

---

**Built with ❤️ using CrewAI, Groq, and Pydantic**
