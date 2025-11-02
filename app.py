import os
import streamlit as st
import mysql.connector
from datetime import datetime
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
import re
import pandas as pd
import base64

# ---------- CONFIG ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "shiva",
    "database": "resume_matcher"
}

# ---------- CACHING MODEL LOAD ----------
@st.cache_resource(show_spinner=False)
def load_embedding_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

model = load_embedding_model()

# ---------- DB UTIL ----------
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def ensure_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        candidate_name VARCHAR(255) NOT NULL,
        candidate_email VARCHAR(255),
        skills_extracted TEXT,
        experience_years VARCHAR(50),
        score FLOAT NOT NULL,
        job_title VARCHAR(255) NOT NULL,
        job_skills TEXT,
        date DATE,
        UNIQUE(candidate_name, job_title)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

ensure_table()

# ---------- HELPERS ----------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

def extract_name(text):
    for line in text.splitlines():
        if line.strip() and not any(word.lower() in line.lower() for word in ["resume", "cv", "curriculum"]):
            if re.match(r"^[A-Za-z][A-Za-z\.\-']{1,40}(\s[A-Za-z][A-Za-z\.\-']{1,40}){0,2}$", line.strip()):
                return line.strip()
    return "Unknown"

SKILLS_LIST = [
    "python","sql","java","c++","javascript","react","node","flask","django",
    "aws","azure","gcp","docker","kubernetes","ml","machine learning","nlp",
    "pandas","numpy","tensorflow","pytorch","scikit-learn","data analysis",
    "excel","power bi","tableau","html","css","rest api","git","linux"
]

def extract_skills(text):
    found = {s.title() for s in SKILLS_LIST if s in text.lower()}
    return sorted(found)

def extract_email(text):
    text = re.sub(r"\\faEnvelope.*?@", "@", text)
    text = re.sub(r"\\href\{mailto:([^}]+)\}", r"\1", text)
    text = re.sub(r"\\color\{[^}]*\}", "", text)
    text = text.replace("mailto:", "").replace("Mailto:", "").replace("MAILTO:", "")
    text = re.sub(r"[^A-Za-z0-9@._%+-]", " ", text)
    match = re.search(r"\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b", text)
    if match:
        email = re.sub(r"^[pme]{0,2}(?=[a-zA-Z0-9._%+-]+@)", "", match.group(1).strip())
        return email
    return None

def extract_job_title_and_skills(job_text):
    lines = [l.strip() for l in job_text.splitlines() if l.strip()]
    lower = job_text.lower()
    title = next((ln for ln in lines[:5] if any(k in ln.lower() for k in 
              ["engineer","analyst","developer","scientist","manager","designer","intern","consultant"])), None)
    if not title and lines:
        title = lines[0][:80]
    job_skills = extract_skills(job_text)
    return title or "General Job", job_skills

def compute_similarity(resume_text, job_text):
    r_emb = model.encode(resume_text, convert_to_tensor=True)
    j_emb = model.encode(job_text, convert_to_tensor=True)
    return round(float(util.pytorch_cos_sim(r_emb, j_emb).item()) * 120, 2)

def save_result_to_db(rec):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM results WHERE candidate_name=%s AND job_title=%s", 
                (rec["candidate_name"], rec["job_title"]))
    if cur.fetchone():
        cur.close(); conn.close(); return False
    query = """INSERT INTO results (candidate_name, candidate_email, skills_extracted, experience_years, 
               score, job_title, job_skills, date)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(query, (
        rec["candidate_name"], rec.get("candidate_email"), ",".join(rec.get("skills_extracted", [])),
        rec.get("experience_years"), rec["score"], rec["job_title"], ",".join(rec.get("job_skills", [])),
        datetime.now().strftime("%Y-%m-%d")
    ))
    conn.commit(); cur.close(); conn.close()
    return True

def fetch_results_for_job(job_title):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT candidate_name, candidate_email, skills_extracted, experience_years, 
               score, job_title, job_skills, date 
        FROM results WHERE job_title=%s ORDER BY score DESC
    """, (job_title,))
    rows = cur.fetchall()
    cur.close(); conn.close()
    cols = ["candidate_name","candidate_email","skills_extracted","experience_years",
            "score","job_title","job_skills","date"]
    return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="AI Resume Matcher", layout="wide")
st.title("🤖 AI Resume Matcher")
st.write("Upload resumes, analyze job descriptions, compute similarity, and view results stored in MySQL.")

tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Recruiter Dashboard", "📈 Dashboard (PDF View)"])

# ---------- TAB 1 ----------
with tab1:
    st.header("Upload Resume & Job Description")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_desc = st.text_area("Paste Job Description", height=200)
    if st.button("Analyze & Save"):
        if not uploaded_file:
            st.warning("Please upload a resume PDF.")
        elif not job_desc.strip():
            st.warning("Please paste the job description.")
        else:
            resume_text = extract_text_from_pdf(uploaded_file)
            candidate_name = extract_name(resume_text)
            candidate_email = extract_email(resume_text)
            skills = extract_skills(resume_text)
            job_title, job_skills = extract_job_title_and_skills(job_desc)
            score = compute_similarity(resume_text, job_desc)

            record = {
                "candidate_name": candidate_name,
                "candidate_email": candidate_email,
                "skills_extracted": skills,
                "experience_years": None,
                "score": score,
                "job_title": job_title,
                "job_skills": job_skills
            }

            saved = save_result_to_db(record)
            st.success(f"Score: {score}% — Saved: {saved}")
            st.markdown(f"**Candidate Name:** {candidate_name}")
            if candidate_email:
                st.markdown(f"**Email:** {candidate_email}")
            st.markdown(f"**Extracted Skills:** {', '.join(skills) if skills else 'None'}")
            st.markdown(f"**Detected Job Title:** {job_title}")
            st.markdown(f"**Job Skills (found):** {', '.join(job_skills) if job_skills else 'None'}")

# ---------- TAB 2 ----------
with tab2:
    st.header("Recruiter Dashboard")
    job_title_filter = st.text_input("Filter by Job Title (exact match)", value="")
    if st.button("Load Results"):
        if not job_title_filter:
            st.info("Enter job title to load results.")
        else:
            df = fetch_results_for_job(job_title_filter)
            if df.empty:
                st.info("No results found for this job title.")
            else:
                st.dataframe(df[["candidate_name","candidate_email","skills_extracted","score","date"]], width="stretch")

# ---------- TAB 3 ----------
with tab3:
    st.header("📊 Power BI Dashboard (PDF Preview)")
    pdf_path = "PowerBI/AI_Resume_Matcher_Dashboard.pdf"

    if os.path.exists(pdf_path):
        st.write("Below is your Power BI dashboard visualization:")
        with open(pdf_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.error("Dashboard PDF not found. Please add 'AI_Resume_Matcher_Dashboard.pdf' to your project folder.")
