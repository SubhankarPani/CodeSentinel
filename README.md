# 🛡️ CodeSentinel — AI-Powered Multi-Agent Code Review System

**CodeSentinel** is an AI-powered code review system that analyzes GitHub Pull Requests using specialized AI agents. It reviews code for style, logical errors, and potential security vulnerabilities, then combines the findings into a structured, developer-friendly report.

Built with **Python, LangChain, Google Gemini, FastAPI, GitHub API, React, and TypeScript**.

---

## 🚀 Overview

Code reviews are an essential part of software development, but manually examining every Pull Request can be time-consuming.

CodeSentinel automates the first level of code review by integrating GitHub Pull Requests with a specialized multi-agent AI architecture.

Instead of relying on a single reviewer, the system uses four AI agents with distinct responsibilities:

- 🎨 **Style Agent:** Reviews code quality, readability, naming conventions, formatting, and maintainability.
- 🧠 **Logic Agent:** Identifies potential logical errors, incorrect conditions, edge cases, and functional issues.
- 🔐 **Security Agent:** Examines code changes for vulnerabilities, exposed secrets, unsafe operations, and insecure patterns.
- 🤖 **Review Agent:** Consolidates findings from the three specialized agents, removes duplicate issues, and generates the final review.

The result is a structured review containing issue severity, category, affected file, line information when available, descriptions, and actionable recommendations.

---

## ✨ Key Features

- **GitHub Pull Request Integration** — Fetches changed files and code diffs directly from GitHub.
- **Multi-Agent Code Review** — Uses specialized AI agents for different review responsibilities.
- **Code Quality Analysis** — Identifies readability, naming, formatting, and maintainability concerns.
- **Logic Analysis** — Examines conditions, calculations, control flow, and edge cases.
- **Security Analysis** — Checks for potentially unsafe code patterns and security vulnerabilities.
- **Finding Consolidation** — Combines agent findings and removes duplicate or overlapping issues.
- **Structured Review Output** — Provides severity, category, file, line, description, and recommendations.
- **Background Processing** — Runs reviews asynchronously through FastAPI background tasks.
- **Review Status Tracking** — Tracks the progress of an individual review job.
- **GitHub Comment Integration** — Can post the generated review directly to the Pull Request when enabled.
- **Interactive Web Interface** — Displays agent progress, individual findings, and the final review.

---

## 🏗️ System Architecture

```text
                  GitHub Pull Request
                           |
                           v
                    GitHub API
                           |
                           v
                 Fetch Changed Files
                     and Diffs
                           |
                           v
                  FastAPI Backend
                           |
                           v
                   Review Service
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        Style Agent   Logic Agent   Security Agent
             |             |             |
             v             v             v
        Style Review  Logic Review  Security Review
             |             |             |
             +-------------+-------------+
                           |
                           v
                     Review Agent
                           |
                 Consolidate Findings
                 Remove Duplicates
                 Generate Final Review
                           |
                           v
                  Structured Review
                           |
                +----------+----------+
                |                     |
                v                     v
          React Frontend       GitHub Comment
          Review Dashboard     (Optional)
```

---

## 🧠 Multi-Agent Workflow

### 1. GitHub Pull Request Retrieval

The user provides:
- GitHub repository name (`owner/repository`)
- Pull Request number

CodeSentinel uses the GitHub API through PyGithub to retrieve the Pull Request's changed files, including available code patches and change information.

### 2. Specialized AI Agents

The review service coordinates three specialized agents.

| Agent | Responsibility |
|---|---|
| Style Agent | Code quality, readability, naming, formatting, and maintainability |
| Logic Agent | Functional correctness, conditions, calculations, control flow, and edge cases |
| Security Agent | Hardcoded secrets, injection risks, unsafe operations, and security vulnerabilities |

Each agent uses a dedicated prompt and Gemini-powered structured output to generate findings.

### 3. Review Agent

The Review Agent receives the findings from all three specialized agents.

It:
- Combines the findings into one review.
- Removes duplicate or overlapping issues.
- Preserves severity and file information when available.
- Avoids introducing unsupported findings.
- Produces concise descriptions and actionable recommendations.

### 4. Final Review

The final result is returned in a structured format using Pydantic models.

Each finding contains:

- Severity: LOW, MEDIUM, or HIGH
- Category
- File
- Line (when identifiable)
- Description
- Recommendation

### 5. GitHub Integration

The final review can be formatted as Markdown and posted as a comment on the original Pull Request.

GitHub comment posting is controlled through the `POST_TO_GITHUB` configuration setting.

---

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Programming Language | Python |
| Agent Framework | LangChain |
| LLM | Google Gemini |
| LLM Integration | langchain-google-genai |
| Backend | FastAPI, Uvicorn |
| GitHub Integration | PyGithub |
| Data Validation | Pydantic |
| Frontend | React, TypeScript |
| Frontend Build Tool | Vite |
| Configuration | Python dotenv |

---

## 📂 Project Structure

```text
CodeSentinel/
│
├── app/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── style_agent.py
│   │   ├── logic_agent.py
│   │   ├── security_agent.py
│   │   └── review_agent.py
│   │
│   ├── github/
│   │   ├── client.py
│   │   ├── formatter.py
│   │   └── tools.py
│   │
│   ├── models/
│   │   └── review.py
│   │
│   ├── services/
│   │   └── review_service.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10+
- Node.js and npm
- Git
- GitHub Personal Access Token
- Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/SubhankarPani/CodeSentinel.git

cd CodeSentinel
```

### 2. Set Up the Backend

Create and activate a virtual environment.

**Windows:**

```bash
python -m venv .venv

.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory.

```env
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_personal_access_token

TEST_MODE=false
POST_TO_GITHUB=false
```

**Configuration:**

| Variable | Description |
|---|---|
| GEMINI_API_KEY | Google Gemini API key used by the AI agents |
| GITHUB_TOKEN | GitHub token used to access Pull Requests |
| TEST_MODE | Enables test mode without Gemini agent calls |
| POST_TO_GITHUB | Enables or disables posting review comments to GitHub |

Keep API credentials private and do not commit your actual `.env` file.

### 4. Start the Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

Backend API:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

### 5. Set Up the Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create a `.env` file inside the `frontend` directory:

```env
VITE_API_URL=http://localhost:8000
```

Start the frontend:

```bash
npm run dev
```

Open the local URL shown by Vite, usually:

```text
http://localhost:5173
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the CodeSentinel API is running |
| GET | `/health` | Health check |
| POST | `/review` | Starts a new Pull Request review |
| GET | `/review/{job_id}` | Retrieves review job status and completed results |

### Start a Code Review

**POST** `/review`

Request:

```json
{
  "repository": "owner/repository",
  "pull_number": 1
}
```

Example response:

```json
{
  "status": "started",
  "job_id": "generated-job-id",
  "message": "CodeSentinel review started."
}
```

### Check Review Status

**GET** `/review/{job_id}`

The endpoint returns the current job status. Once completed, it includes the individual agent findings and the consolidated review.

Possible workflow statuses include:

```text
queued
fetching_pr
style_running
style_completed
logic_running
logic_completed
security_running
security_completed
review_running
review_completed
completed
failed
```

---

## 🖥️ Web Interface

The React frontend provides an interface to:

1. Enter a GitHub repository and Pull Request number.
2. Start an AI-powered code review.
3. Track the review process.
4. View findings from the Style, Logic, and Security agents.
5. Inspect the consolidated final review.
6. Open the GitHub comment when one has been posted.

The frontend polls the backend review-status endpoint while the background review is running.

---

## 🔍 Structured Review Output

CodeSentinel uses Pydantic models to keep the review output consistent.

Example finding:

```json
{
  "severity": "HIGH",
  "category": "Security",
  "file": "app/example.py",
  "line": "25",
  "description": "Potentially unsafe use of user-controlled input.",
  "recommendation": "Validate and sanitize the input before processing it."
}
```

The example above illustrates the output structure; it is not a claim about a specific detected vulnerability.

---

## ⚡ Reliability and Error Handling

The Gemini integration includes:
- Configurable request timeout.
- Retry handling for temporary failures.
- Exponential backoff between retry attempts.
- Detection of quota and rate-limit errors.
- Structured output using Pydantic models.

CodeSentinel also includes a `TEST_MODE` configuration to run a predefined test review without making Gemini API calls.

---

## 🔮 Future Enhancements

Potential improvements include:

- GitHub Webhook integration for automatic PR reviews.
- Inline review comments linked to specific code lines.
- More specialized agents for performance and testing.
- Improved review history and persistent job storage.
- More robust authentication and authorization.
- Additional language-specific review capabilities.
- Automated CI/CD integration.

---

## ⚠️ Project Notes

- AI-generated findings should be reviewed by developers before changes are made.
- CodeSentinel provides AI-assisted review, not a replacement for human code review or dedicated security testing.
- Review jobs are currently stored in application memory, so they are not persistent across backend restarts.
- GitHub comment posting is optional and disabled by default.
- The quality of findings depends on the available Pull Request diff and the LLM response.

---

## 👨‍💻 Author

**Subhankar Pani**

GitHub: [@SubhankarPani](https://github.com/SubhankarPani)

Project: [CodeSentinel](https://github.com/SubhankarPani/CodeSentinel)

---

⭐ If you find this project interesting, feel free to explore the repository and share feedback.

**CodeSentinel — Making Code Reviews Smarter with AI.**
