from crewai import Task
from agents import researcher, analyst
from tools import tool

research_task=Task(
    description=(
        "Use the provided URL ({url}) to fetch and extract the main body text of the news article. "
        "Include the title, author (if available), publication date, and all main text paragraphs. "
        "Remove unrelated content like ads, navigation, and comments. "
        "Provide the clean article text as your output."
    ),
    expected_output=(
        "Do not show the thinking, just provide me a clean, plain-text version of the article including title, author, date, and main content."
    ),
    agent=researcher,
    tools=[tool]
)

analysis_task=Task(
    description=(
        "Analyze the provided news article text  with the following sections:\n"
        "1. Core Claims — 3–5 main factual claims from the article.\n"
        "2. Language & Tone Analysis — describe and classify tone (neutral, emotional, persuasive, etc.).\n"
        "3. Potential Red Flags — list indicators of bias or weak reporting.\n"
        "4. Verification Questions — 3–4 questions the reader should ask to verify claims.\n"
        "BONUS: Perform Named Entity Recognition to identify key people, organizations, and locations, and suggest what to investigate.\n"
        "BONUS: Summarize the article from a hypothetical opposing viewpoint."
    ),
    expected_output=(
        "Do not show the thinking. just create a well-formatted text report containing all sections and dont include \"#\" or \"*\" to mark different sections just use good spacing, saved to output/report.txt."
    ),
    agent=analyst,
    context=[research_task],
    output_file="output/report.txt"
)
