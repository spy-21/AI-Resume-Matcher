# 🤖 AI Resume Matcher

An **AI-powered Resume Screening System** that automatically analyzes resumes, extracts candidate details, and matches them to job descriptions using **semantic similarity**.  
All analyzed data is stored in **MySQL**, and recruiter analytics are displayed through an embedded **Power BI dashboard**.

---

## 🚀 Features

- 📂 Upload resumes (PDF)
- 🧠 Extract candidate name, email, and technical skills
- 🔎 Analyze job description automatically
- 📊 Compute AI-based similarity score using **Sentence Transformers**
- 🗃️ Store results securely in **MySQL**
- 🖥️ Recruiter dashboard for viewing & filtering candidates
- 📈 Integrated **Power BI Dashboard (PDF View)** for analytics
- 📧 Automated emails sent to shortlisted candidates (score ≥ 40%)

---

## 🧩 System Architecture

```
📄 Resume (PDF)
   ↓
🔍 Text Extraction → PyPDF2
   ↓
🧠 Semantic Matching → SentenceTransformer (all-MiniLM-L6-v2)
   ↓
🗃️ Database Storage → MySQL
   ↓
🌐 Frontend → Streamlit Web App
   ↓
📈 Visualization → Power BI (Embedded PDF View)
```

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
venv\Scripts\activate    # On Windows
source venv/bin/activate # On macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet:

```bash
pip install streamlit mysql-connector-python sentence-transformers PyPDF2 pandas python-dotenv
```

---

### 4️⃣ Configure MySQL

Open MySQL and create the database:

```sql
CREATE DATABASE resume_matcher;
```

Then update your database credentials in `app.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "resume_matcher"
}
```

---

### 5️⃣ Configure Email Automation

Create a file named `.env` in your project folder:

```
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```

📌 **Note:**  
Use an **App Password** (from Google Account → Security → App Passwords) instead of your actual Gmail password.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open your browser and go to:  
👉 [http://localhost:8501](http://localhost:8501)

---

## 🧮 Tech Stack

| Layer          | Technology                                 | Purpose                                                  |
| -------------- | ------------------------------------------ | -------------------------------------------------------- |
| Frontend       | **Streamlit**                              | User interface for uploading resumes & viewing analytics |
| Backend        | **Python 3.10+**                           | Core logic, NLP processing, and database integration     |
| AI Model       | **SentenceTransformer (all-MiniLM-L6-v2)** | Computes semantic similarity between resume & job        |
| Database       | **MySQL**                                  | Stores results & candidate information                   |
| PDF Processing | **PyPDF2**                                 | Extracts text from resumes                               |
| Visualization  | **Power BI (Embedded PDF)**                | Displays recruiter analytics & score distribution        |
| Data Handling  | **Pandas, Regex, Base64**                  | Cleansing, extraction, and rendering                     |
| Automation     | **smtplib + dotenv**                       | Sends emails securely using environment variables        |

---

## 📊 Power BI Dashboard Integration

- Place your Power BI dashboard PDFs in the `PowerBI/` folder
- Example structure:
  ```
  PowerBI/
  ├── AI_Resume_Matcher_Dashboard.pdf
  ├── AI_Resume_Matcher_Dashboardsec.pdf
  ├── AI_Resume_Matcher_Dashboardthird.pdf
  ```
- Inside the Streamlit app (Tab 3), you can **select which dashboard to view** from a dropdown list.

---

## 👨‍💻 Developer

**Developed by:** [Katagoni Shiva Prasad](mailto:shivaprasad21072003@gmail.com)  
📧 Email: [shivaprasad21072003@gmail.com](mailto:shivaprasad21072003@gmail.com)  
💼 GitHub: [spy-21](https://github.com/spy-21)
