import { useState } from "react";
import "./App.css";

interface ReviewIssue {
  severity: string;
  category: string;
  file: string | null;
  line: string | null;
  description: string;
  recommendation: string;
}

interface AgentReview {
  issues: ReviewIssue[];
}

interface ReviewResult {
  status: string;
  repository: string;
  pull_number: number;
  issues_found: number;
  comment_url: string | null;

  agents: {
    style: AgentReview;
    logic: AgentReview;
    security: AgentReview;
    final: AgentReview;
  };

  review: AgentReview;
}

interface JobResponse {
  job_id: string;
  status: string;
  result?: ReviewResult;
  error?: string;
}

function App() {
  const [repository, setRepository] = useState(
    "SubhankarPani/CodeSentinel"
  );

  const [pullNumber, setPullNumber] = useState("1");

  const [loading, setLoading] = useState(false);

  const [jobStatus, setJobStatus] = useState("");

  const [result, setResult] =
    useState<ReviewResult | null>(null);

  const [error, setError] = useState("");

  const agents = [
    {
      name: "Style Agent",
      key: "style" as const,
      runningStatus: "style_running",
      completedStatus: "style_completed",
      description:
        "Checks code quality, readability and coding style.",
    },
    {
      name: "Logic Agent",
      key: "logic" as const,
      runningStatus: "logic_running",
      completedStatus: "logic_completed",
      description:
        "Checks logic, conditions, edge cases and correctness.",
    },
    {
      name: "Security Agent",
      key: "security" as const,
      runningStatus: "security_running",
      completedStatus: "security_completed",
      description:
        "Checks vulnerabilities, secrets and unsafe code.",
    },
  ];

  const pollJobStatus = async (jobId: string) => {
    const maxAttempts = 60;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/review/${jobId}`
        );

        const data: JobResponse =
          await response.json();

        if (!response.ok) {
          throw new Error(
            data.error || "Failed to get review status"
          );
        }

        setJobStatus(data.status);

        if (data.status === "completed") {
          setResult(data.result || null);
          setLoading(false);
          return;
        }

        if (data.status === "failed") {
          throw new Error(
            data.error || "CodeSentinel review failed"
          );
        }

        await new Promise((resolve) =>
          setTimeout(resolve, 2000)
        );
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Something went wrong"
        );

        setLoading(false);
        return;
      }
    }

    setError(
      "Review is taking too long. Please try again."
    );

    setLoading(false);
  };

  const handleReview = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    setJobStatus("starting");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/review",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            repository: repository,
            pull_number: Number(pullNumber),
          }),
        }
      );

      const data: JobResponse =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Failed to start review"
        );
      }

      setJobStatus("queued");

      await pollJobStatus(data.job_id);

    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong"
      );

      setLoading(false);
    }
  };

  const renderIssue = (
    issue: ReviewIssue,
    index: number
  ) => {
    return (
      <div
        className="agent-issue"
        key={index}
      >
        <div className="issue-header">

          <span className="severity">
            {issue.severity}
          </span>

          <span className="category">
            {issue.category}
          </span>

        </div>

        {issue.file && (
          <p>
            <strong>File:</strong>{" "}
            {issue.file}
          </p>
        )}

        {issue.line && (
          <p>
            <strong>Line:</strong>{" "}
            {issue.line}
          </p>
        )}

        <h4>Description</h4>

        <p>
          {issue.description}
        </p>

        <h4>Recommendation</h4>

        <p>
          {issue.recommendation}
        </p>
      </div>
    );
  };

  return (
    <div className="app">

      <header className="header">

        <h1>
          CodeSentinel 🤖
        </h1>

        <p>
          AI-Powered GitHub Pull Request Code Review
        </p>

      </header>

      <main className="container">

        <section className="review-form">

          <label>
            GitHub Repository
          </label>

          <input
            type="text"
            value={repository}
            onChange={(e) =>
              setRepository(e.target.value)
            }
            placeholder="owner/repository"
            disabled={loading}
          />

          <label>
            Pull Request Number
          </label>

          <input
            type="number"
            value={pullNumber}
            onChange={(e) =>
              setPullNumber(e.target.value)
            }
            placeholder="1"
            disabled={loading}
          />

          <button
            onClick={handleReview}
            disabled={loading}
          >
            {loading
              ? "Reviewing PR..."
              : "Review Pull Request"}
          </button>

        </section>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {loading && (
          <div className="loading">

            🤖 CodeSentinel is analyzing the
            Pull Request...

            <p>
              Status:{" "}
              <strong>
                {jobStatus}
              </strong>
            </p>

          </div>
        )}

        {result && (
          <section className="results">

            <div className="agent-pipeline">

              <h2>
                AI Review Pipeline
              </h2>

              <div className="agents">

                {agents.map((agent) => {

                                const isRunning =
                                  jobStatus === agent.runningStatus;

                                const isCompleted =
                                  jobStatus === agent.completedStatus ||
                                  result !== null;

                                return (
                                  <div
                                      className={`agent ${
                                        jobStatus === "review_running"
                                          ? "agent-running"
                                          : jobStatus === "review_completed" ||
                                            result !== null
                                          ? "agent-completed"
                                          : "agent-pending"
                                      }`}
                                    >

                                      <div className="agent-check">

                                        {jobStatus === "review_running"
                                          ? "⟳"
                                          : jobStatus === "review_completed" ||
                                            result !== null
                                          ? "✓"
                                          : "○"}

                                      </div>

                                      <strong>
                                        Review Agent
                                      </strong>

                                      <p>

                                        {jobStatus === "review_running"
                                          ? "Combining findings..."
                                          : jobStatus === "review_completed" ||
                                            result !== null
                                          ? "Completed"
                                          : "Waiting..."}

                                      </p>

                                    </div>
                                );
                              })}

                <div className="agent review-agent">

                  <div className="agent-check">
                    ✓
                  </div>

                  <strong>
                    Review Agent
                  </strong>

                  <p>
                    Combines all findings into
                    the final review.
                  </p>

                </div>

              </div>

            </div>

            <div className="specialist-section">

              <h2>
                Agent Findings
              </h2>

              {agents.map((agent) => {

                const agentReview =
                  result.agents[agent.key];

                return (
                  <div
                    className="agent-result"
                    key={agent.key}
                  >

                    <div className="agent-result-header">

                      <div>

                        <h3>
                          {agent.name}
                        </h3>

                        <p>
                          {agent.description}
                        </p>

                      </div>

                      <span className="finding-count">

                        {agentReview.issues.length}{" "}

                        {agentReview.issues.length === 1
                          ? "finding"
                          : "findings"}

                      </span>

                    </div>

                    {agentReview.issues.length === 0 ? (

                      <div className="no-issues">

                        ✓ No issues found by this agent.

                      </div>

                    ) : (

                      <div className="agent-issues">

                        {agentReview.issues.map(
                          renderIssue
                        )}

                      </div>

                    )}

                  </div>
                );
              })}

            </div>

            <div className="final-review">

              <div className="results-header">

                <h2>
                  Final Review
                </h2>

                <span>
                  {result.issues_found} issue(s) found
                </span>

              </div>

              {result.review.issues.map(
                (issue, index) => (

                  <div
                    className="issue-card"
                    key={index}
                  >

                    <div className="issue-header">

                      <span className="severity">
                        {issue.severity}
                      </span>

                      <span className="category">
                        {issue.category}
                      </span>

                    </div>

                    {issue.file && (
                      <p>
                        <strong>
                          File:
                        </strong>{" "}
                        {issue.file}
                      </p>
                    )}

                    {issue.line && (
                      <p>
                        <strong>
                          Line:
                        </strong>{" "}
                        {issue.line}
                      </p>
                    )}

                    <h3>
                      Description
                    </h3>

                    <p>
                      {issue.description}
                    </p>

                    <h3>
                      Recommendation
                    </h3>

                    <p>
                      {issue.recommendation}
                    </p>

                  </div>
                )
              )}

            </div>

            {result.comment_url && (
              <a
                href={result.comment_url}
                target="_blank"
                rel="noreferrer"
                className="github-link"
              >
                View GitHub Comment →
              </a>
            )}

          </section>
        )}

      </main>

    </div>
  );
}

export default App;