from crewai import Crew,Process
from tasks import research_task, analysis_task
from agents import researcher, analyst

crew=Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    process=Process.sequential,
)

result=crew.kickoff(inputs={"url": "https://indianexpress.com/article/india/express-report-prashant-kishor-enrolled-voter-2-notice-10331936/?ref=breaking_hp"})
print(result)