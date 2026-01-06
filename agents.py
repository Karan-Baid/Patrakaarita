from crewai import Agent
from dotenv import load_dotenv
load_dotenv()
import os
from tools import tool

# Using Groq for excellent rate limits (30 RPM) and blazing fast inference
llm = "groq/llama-3.3-70b-versatile"

researcher=Agent(
    role="Web Content Extractor",
    goal="Retrieve and cleanly extract news article content from the given URL.",
    backstory="Expert in extracting online content for AI analysis, with experience in filtering out noise.",
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,  # Prevent delegation to reduce API calls
    tools=[tool]
)

analyst=Agent(
    role="AI Critical Thinking Partner",
    goal="Analyze an article for factual claims, tone, biases, and verification questions — without making truth judgments.",
    backstory="Skilled in media literacy, bias detection, and structured reporting for online news content.",
    llm=llm,
    verbose=False,  # Reduce verbosity to minimize API calls
    memory=False,    # Disable memory to reduce API calls
    allow_delegation=False
)
    
