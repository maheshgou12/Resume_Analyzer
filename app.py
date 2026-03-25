import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os

from resume_parser import extract_text_from_pdf
from preprocessing import clean_text
from matcher import extract_skills, match_jobs

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ===== PROFESSIONAL UI =====
st.markdown("""
<style>
.main {
    background-color: #f4f6f8;
}
h1 {
    color: #2c3e50;
}
.card {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    padding:20px;
    border-radius:12px;
    color:white;
    text-align:center;
    font-size:28px;
}
</style>
""", unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer & Job Matcher")

# ===== SIDEBAR =====
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Analyzer","History","Ranking","Analytics"]
)

scores_list = []
names_list = []

# ================= ANALYZER =================
   


   # ================= ANALYZER =================
if page == "Analyzer":

    uploaded_files = st.file_uploader(
        "Upload resume(s) (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:

            st.divider()
            st.subheader(f"📄 Resume: {uploaded_file.name}")

            raw_text = extract_text_from_pdf(uploaded_file)
            cleaned_text = clean_text(raw_text)

            # ===== SKILLS =====
            skills = extract_skills(cleaned_text)
            st.write("✅ Extracted Skills:", skills)

            # ===== PROFESSIONAL SKILL DISPLAY =====
            st.subheader("🔎 Detected Resume Skills")

            skills_html = ""
            for skill in skills:
                skills_html += f"""
                <span style="
                    background:#28a745;
                    color:white;
                    padding:6px 12px;
                    border-radius:10px;
                    margin:5px;
                    display:inline-block;
                    font-size:14px;">
                    {skill}
                </span>
                """

            st.markdown(skills_html, unsafe_allow_html=True)

            st.subheader("📄 Resume Preview")
            st.text_area(
                "Extracted Resume Content",
                raw_text[:1200],
                height=250
            )

            # ===== JOB MATCH =====
            job_matches = match_jobs(cleaned_text)

            resume_score = int(job_matches["match_percentage"].max())

            # ===== SCORE CARD =====
            st.markdown(
                f'<div class="card">Resume Score : {resume_score}/100</div>',
                unsafe_allow_html=True
            )

            # ===== SCORE GRAPH =====
            fig, ax = plt.subplots()
            ax.bar(["Match Score"], [resume_score])
            ax.set_ylim(0, 100)
            st.pyplot(fig)

            st.dataframe(job_matches)

            top_job = job_matches.iloc[0]

            st.success(
                f"🏆 Best Match: {top_job['job_title']} "
                f"({top_job['match_percentage']}%)"
            )

            # ===== CAREER RECOMMENDATION =====
            st.subheader("🎯 Career Recommendation")

            if "machine learning" in skills:
                st.success("🤖 Recommended Career: Machine Learning Engineer")
            elif "python" in skills and "sql" in skills:
                st.success("📊 Recommended Career: Data Analyst")
            elif "html" in skills or "css" in skills:
                st.success("🌐 Recommended Career: Web Developer")
            elif "java" in skills:
                st.success("☕ Recommended Career: Java Developer")
            else:
                st.info("Explore Software Development roles")

            # ===== SAVE HISTORY =====
            history_data = pd.DataFrame({
                "resume_name":[uploaded_file.name],
                "score":[resume_score],
                "best_job":[top_job["job_title"]],
                "skills":[", ".join(skills)]
            })

            if not os.path.isfile("history.csv"):
                history_data.to_csv("history.csv", index=False)
            else:
                history_data.to_csv(
                    "history.csv",
                    mode="a",
                    header=False,
                    index=False
                )  
# ================= HISTORY =================
if page == "History":

    st.title("📁 Resume Analysis History")

    if os.path.isfile("history.csv"):
        df = pd.read_csv("history.csv")
        st.dataframe(df)
    else:
        st.warning("No history available")

# ================= RANKING =================
if page == "Ranking":

    st.title("🏆 Resume Ranking System")

    if os.path.isfile("history.csv"):
        df = pd.read_csv("history.csv")

        ranking_df = df.sort_values(
            by="score",
            ascending=False
        )

        st.dataframe(ranking_df)

        fig, ax = plt.subplots()
        ax.bar(ranking_df["resume_name"], ranking_df["score"])
        plt.xticks(rotation=45)
        st.pyplot(fig)

    else:
        st.warning("No ranking data available")

# ================= ANALYTICS =================
if page == "Analytics":

    st.title("📊 Resume Analytics Dashboard")

    if os.path.isfile("history.csv"):

        df = pd.read_csv("history.csv")

        # total resumes
        st.metric("Total Resumes", len(df))

        # average score
        st.metric("Average Score", int(df["score"].mean()))

        # score distribution
        st.subheader("📈 Score Distribution")
        fig1, ax1 = plt.subplots()
        ax1.hist(df["score"])
        st.pyplot(fig1)

        # skill frequency
        st.subheader("🔥 Top Skills")

        from collections import Counter

        skills_series = df["skills"].str.split(", ")
        all_skills = []

        for skill_list in skills_series:
            all_skills.extend(skill_list)

        skill_count = Counter(all_skills)

        fig2, ax2 = plt.subplots()
        ax2.bar(skill_count.keys(), skill_count.values())
        plt.xticks(rotation=60)
        st.pyplot(fig2)

    else:
        st.warning("No analytics data available")