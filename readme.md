# 🤖 AI Resume Matcher

An **AI-powered Resume Screening System** that analyzes resumes, extracts candidate information, and matches them to job descriptions using **semantic similarity**.  
All results are stored in **MySQL**, and recruiter analytics are displayed through an embedded **Power BI dashboard**.

---

## 🚀 Features

- 🔄 Upload and process resumes (PDF)
- 🧠 Extract candidate name, email, and technical skills
- 🔎 Analyze job description automatically
- 📊 Compute AI-based similarity score using **Sentence Transformers**
- 🗃️ Store results in **MySQL** database
- 🗾 View recruiter dashboard inside Streamlit
- 📈 Integrated **Power BI Dashboard (PDF View)** for visualization

---

## 🏗️ System Architecture

```
📄 Resume (PDF)
   ↓
🔍 Text Extraction → PyPDF2
   ↓
🧠 Similarity Analysis → SentenceTransformer (all-MiniLM-L6-v2)
   ↓
🗃️ Data Storage → MySQL Database
   ↓
🌐 Frontend → Streamlit Web App
   ↓
📈 Visualization → Power BI Dashboard
```

---

## 🧮 Tech Stack

| Layer         | Technology                                   | Purpose                                           |
| ------------- | -------------------------------------------- | ------------------------------------------------- |
| Frontend      | **Streamlit**                                | UI for uploading resumes and viewing analytics    |
| Backend       | **Python 3.10+**                             | Core logic, ML processing, DB integration         |
| AI Model      | **SentenceTransformer (`all-MiniLM-L6-v2`)** | Computes semantic similarity between resume & job |
| Database      | **MySQL**                                    | Stores candidate results and job data             |
| PDF Parser    | **PyPDF2**                                   | Extracts raw text from uploaded resumes           |
| Visualization | **Power BI (PDF)**                           | Displays analytics & scoring overview             |
| Data Handling | **Pandas, Regex, Base64**                    | Cleansing, formatting, and rendering              |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/spy-21/ai-resume-matcher.git
cd ai-resume-matcher
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a requirements file yet, use:

```bash
pip install streamlit mysql-connector-python sentence-transformers PyPDF2 pandas
```

### 4️⃣ Configure MySQL

Create the database:

```sql
CREATE DATABASE resume_matcher;
```

Update the `DB_CONFIG` in `app.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "resume_matcher"
}
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open:  
🔗 [http://localhost:8501](http://localhost:8501)

---

## 🧩 How It Works

1. Upload a **resume PDF**
2. Paste the **job description**
3. App extracts name, email, and skills
4. AI model compares resume and job text → generates a **similarity score**
5. Results are saved in **MySQL**
6. Recruiter can:
   - Filter results by job title
   - View Power BI PDF dashboard for analytics

---

## 📊 Power BI Dashboard

- The dashboard file is located at:
  ```
  PowerBI/AI_Resume_Matcher_Dashboard.pdf
  ```
- It is **embedded inside the Streamlit app** (Tab: "Dashboard (PDF View)")

---

## 🧮 Example Output

| Candidate Name        | Email                     | Score | Job Title                          | Skills Extracted       |
| --------------------- | ------------------------- | ----- | ---------------------------------- | ---------------------- |
| Katagoni Shiva Prasad | shivaprasad21@gmail.com   | 53.63 | AI Application Developer           | Flask, Python, SQL, ML |
| Kurapati Aravind      | kurapatiaravind@gmail.com | 49.65 | Machine Learning Engineer – Intern | Flask, Git, ML, Python |

---

## 🤓 AI Logic Behind Matching

- Uses **SentenceTransformer** (`all-MiniLM-L6-v2`)
- Generates vector embeddings for both resume and job description
- Calculates **Cosine Similarity**
- Outputs a score between **0–100%**
  - Higher = Stronger match
  - Lower = Less relevant

---

## 🗂️ Folder Structure

```
AI-Resume-Matcher/
│
├── app.py                        # Main Streamlit application
├── PowerBI/
│   └── AI_Resume_Matcher_Dashboard.pdf  # Dashboard visualization
├── requirements.txt
└── README.md
```

---

## 🔬 Future Enhancements

- 🔐 Add authentication (Admin / Recruiter login)
- 📩 Send automated emails to candidates
- 🌐 Connect **live Power BI dashboard** using Power BI API
- 📊 Add real-time charts in Streamlit
- ☁️ Deploy on AWS / Streamlit Cloud

---

## 👨‍💻 Developer

**Developed by:** Katagoni Shiva Prasad  
📧 Email: [shivaprasad21072003@gmail.com](mailto:shivaprasad21072003@gmail.com)
