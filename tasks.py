from crewai import Task
from pydantic import BaseModel, Field
from agents import researcher, analyst
from tools import tool


class ResearchOutput(BaseModel):
    title: str = Field(description="Article title")
    author: str = Field(default="", description="Author name if available")
    publication_date: str = Field(default="", description="Publication date")
    main_content: str = Field(description="Clean article text without ads, navigation, or comments")


class AnalysisOutput(BaseModel):
    core_claims: list[str] = Field(
        description="3-5 main factual claims from the article",
        min_length=3,
        max_length=5
    )
    tone_analysis: str = Field(
        description="Language and tone classification (neutral, emotional, persuasive, etc.)"
    )
    red_flags: list[str] = Field(
        description="List of indicators of bias or weak reporting"
    )
    verification_questions: list[str] = Field(
        description="3-4 questions the reader should ask to verify claims",
        min_length=3,
        max_length=4
    )
    named_entities: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Key people, organizations, and locations identified in the article"
    )
    opposing_viewpoint: str = Field(
        default="",
        description="Summary of the article from a hypothetical opposing viewpoint"
    )


research_task = Task(
    description=(
        "Use the provided URL ({url}) to fetch and extract the main body text of the news article. "
        "Include the title, author (if available), publication date, and all main text paragraphs. "
        "Remove unrelated content like ads, navigation, and comments."
    ),
    expected_output="Structured article data with title, author, date, and clean main content.",
    agent=researcher,
    tools=[tool],
    output_pydantic=ResearchOutput
)

analysis_task = Task(
    description=(
        "Analyze the provided news article text with the following sections:\n"
        "1. Core Claims — 3–5 main factual claims from the article.\n"
        "2. Language & Tone Analysis — describe and classify tone (neutral, emotional, persuasive, etc.).\n"
        "3. Potential Red Flags — list indicators of bias or weak reporting.\n"
        "4. Verification Questions — 3–4 questions the reader should ask to verify claims.\n"
        "BONUS: Perform Named Entity Recognition to identify key people, organizations, and locations.\n"
        "BONUS: Summarize the article from a hypothetical opposing viewpoint."
    ),
    expected_output="Structured analysis with core claims, tone analysis, red flags, verification questions, named entities, and opposing viewpoint.",
    agent=analyst,
    context=[research_task],
    output_pydantic=AnalysisOutput
)
