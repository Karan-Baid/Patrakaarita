
from crewai import Crew, Process
from tasks import research_task, analysis_task, ResearchOutput, AnalysisOutput
from agents import researcher, analyst

def run_crew_for_url(url: str):
    crew = Crew(
        agents=[researcher, analyst],
        tasks=[research_task, analysis_task],
        process=Process.sequential,
    )
    return crew.kickoff(inputs={"url": url})

if __name__ == "__main__":
    # For CLI usage, you can still run a sample URL here if desired
    sample_url = "https://indianexpress.com/article/india/express-report-prashant-kishor-enrolled-voter-2-notice-10331936/?ref=breaking_hp"
    result = run_crew_for_url(sample_url)
    
    # Display structured outputs
    print("\n" + "="*60)
    print("RESEARCH OUTPUT")
    print("="*60)
    if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
        research_output = result.tasks_output[0].pydantic
        if isinstance(research_output, ResearchOutput):
            print(f"Title: {research_output.title}")
            print(f"Author: {research_output.author}")
            print(f"Date: {research_output.publication_date}")
            print(f"\nContent Preview: {research_output.main_content[:200]}...")
    
    print("\n" + "="*60)
    print("ANALYSIS OUTPUT")
    print("="*60)
    if hasattr(result, 'tasks_output') and len(result.tasks_output) > 1:
        analysis_output = result.tasks_output[1].pydantic
        if isinstance(analysis_output, AnalysisOutput):
            print(f"Core Claims: {len(analysis_output.core_claims)}")
            for i, claim in enumerate(analysis_output.core_claims, 1):
                print(f"  {i}. {claim}")
            print(f"\nTone: {analysis_output.tone_analysis}")
            print(f"\nRed Flags: {len(analysis_output.red_flags)}")
            for i, flag in enumerate(analysis_output.red_flags, 1):
                print(f"  {i}. {flag}")