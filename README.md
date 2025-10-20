# 🧠 UniPath AI Agent

UniPath AI Agent is an intelligent academic guidance system that helps students analyze their resumes, match them with suitable graduate programs, and discover relevant professors — all powered by **LLMs (AWS Bedrock + Anthropic Claude)** and a **FastAPI + Vue.js** tech stack.

---

## 🚀 Features

### 🎓 Resume Analysis
- Upload your resume (PDF)
- Automatically extracts education, skills, research interests, and publications
- Summarizes key academic background in structured JSON

### 🎯 Program Recommendation
- Finds graduate programs that align with your field of study
- Displays program name, snippet, and direct application link

### 👩‍🏫 Faculty Matching
- Matches you with professors whose research interests align with your resume
- Fetches faculty names, titles, and research areas dynamically

### 📄 Requirement Parser
- Parses university program pages (via URL)
- Extracts key application requirements (GPA, GRE, deadlines, etc.)

### 📊 Progress Tracker *(optional extension)*
- Tracks application progress and stores user profiles via unique user IDs

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Vue 3 + Vite |
| **Backend** | FastAPI (Python) |
| **AI Engine** | AWS Bedrock + Anthropic Claude 3.5 |
| **Data Extraction** | PyMuPDF, BeautifulSoup |
| **Storage** | AWS S3 |
| **Infra / Dev** | boto3, dotenv, requests, JSON pipelines |

---

## ⚙️ Project Structure

