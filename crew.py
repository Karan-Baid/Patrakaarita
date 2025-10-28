
from crewai import Crew, Process
from tasks import research_task, analysis_task
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
    print(result)