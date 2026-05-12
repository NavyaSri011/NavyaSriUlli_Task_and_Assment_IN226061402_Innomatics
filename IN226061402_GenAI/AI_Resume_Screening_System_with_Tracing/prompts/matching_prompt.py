from langchain_core.prompts import PromptTemplate

matching_prompt = PromptTemplate(
    input_variables=["resume_skills", "job_description"],
    template="""
You are an expert ATS (Applicant Tracking System).

Compare the resume skills with the job description.

Resume Skills:
{resume_skills}

Job Description:
{job_description}

Task:
- Identify matched skills
- Identify missing skills
- Calculate match percentage (0-100)

Return ONLY valid JSON:

{{
  "matched_skills": [],
  "missing_skills": [],
  "match_percentage": number
}}
"""
)