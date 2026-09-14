# CodeSentinel
CodeSentinel — An autonomous multi-agent AI code review system that analyzes GitHub pull requests using specialized Style, Logic, and Security agents powered by LLM reasoning and ReAct-based tool orchestration.

# 🛡️ CodeSentinel

### Autonomous Multi-Agent AI Code Review System

> CodeSentinel is an AI-powered code review system that automatically analyzes GitHub Pull Requests using specialized AI agents for Style, Logic, and Security, and generates a consolidated developer-friendly review.

---

## 🚀 Overview

Code review is an important part of software development, but manually reviewing every Pull Request can be time-consuming.

**CodeSentinel** automates the first level of code review by combining the GitHub API with a multi-agent AI architecture.

Instead of relying on a single AI reviewer, CodeSentinel uses multiple specialized agents:

- 🎨 **Style Agent** — analyzes code quality, complexity, readability, and maintainability.
- 🧠 **Logic Agent** — analyzes logic, behavior, and potential performance problems.
- 🔐 **Security Agent** — looks for potentially unsafe patterns and security concerns.
- 🤖 **Review Agent** — combines the findings, removes duplicate or overlapping issues, and produces the final review.

The goal is to provide developers with a fast and structured **AI-assisted first-pass code review**.

---

## ✨ Key Features

- 🔗 **GitHub Pull Request Integration**
- 🤖 **Multi-Agent AI Code Review**
- 🎨 **Style & Maintainability Analysis**
- 🧠 **Logic & Performance Analysis**
- 🔐 **Security Analysis**
- 🔄 **Finding Consolidation & Deduplication**
- 📋 **Structured Review Results**
- ⚡ **Automated End-to-End Review Pipeline**
- 🌐 **Web Interface** *(planned)*

---

# 🏗️ Architecture

```text
                    GitHub Pull Request
                            │
                            ▼
                     ┌─────────────┐
                     │  GitHub API │
                     └──────┬──────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   CodeSentinel  │
                   │  Review Service │
                   └────────┬────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       ┌───────────┐  ┌───────────┐  ┌────────────┐
       │   Style   │  │   Logic   │  │  Security  │
       │   Agent   │  │   Agent   │  │   Agent    │
       └─────┬─────┘  └─────┬─────┘  └──────┬─────┘
             │              │               │
             └──────────────┼───────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Review Agent   │
                   │                 │
                   │ Deduplicate     │
                   │ Consolidate     │
                   │ Finalize        │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Final Review   │
                   │     Report      │
                   └─────────────────┘
