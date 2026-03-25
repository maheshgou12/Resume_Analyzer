import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills_list import SKILLS


def extract_skills(text):
    found_skills = []
    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)
    return list(set(found_skills))


def get_missing_skills(resume_skills, job_description):
    job_words = job_description.lower().split()
    missing = list(set(job_words) - set(resume_skills))
    return missing[:5]


def match_jobs(resume_text, job_csv_path="data/job_descriptions.csv"):
    jobs = pd.read_csv(job_csv_path)

    job_texts = jobs["job_description"].tolist()

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text] + job_texts)

    similarity_scores = cosine_similarity(
        vectors[0:1], vectors[1:]
    ).flatten()

    jobs["match_percentage"] = (similarity_scores * 100).round(2)

    jobs = jobs.sort_values(
        by="match_percentage", ascending=False
    )

    return jobs[["job_title", "match_percentage"]]

def get_missing_skills(resume_skills, job_description):

    job_words = job_description.lower().split()

    missing = list(set(job_words) - set(resume_skills))

    return missing[:5]



