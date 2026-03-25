
from resume_parser import extract_text_from_pdf
from preprocessing import clean_text
from matcher import extract_skills, match_jobs

with open("test_resumes/resume.pdf", "rb") as file:
    raw_text = extract_text_from_pdf(file)

cleaned_text = clean_text(raw_text)

skills = extract_skills(cleaned_text)
print("EXTRACTED SKILLS:\n", skills)


job_matches = match_jobs(cleaned_text)
print("\nJOB MATCH RESULTS:\n")
print(job_matches)

