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

interface ReviewResponse {
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

function App() {
  const [repository, setRepository] = useState(
    "SubhankarPani/CodeSentinel"
  );

  const [pullNumber, setPullNumber] = useState("1");

  const [loading, setLoading] = useState(false);

  const [result, setResult] =
    useState<ReviewResponse | null>(null);

  const [error, setError] = useState("");

  const handleReview = async () => {
    setLoading(true);
    setError("");
    setResult(null);

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

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Review failed"
        );
      }

      setResult(data);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  const agents = [
    {
      name: "Style Agent",
      key: "style" as const,
      description:
        "Checks code quality, readability and coding style.",
    },
    {
      name: "Logic Agent",
      key: "logic" as const,
      description:
        "Checks logic, conditions, edge cases and correctness.",
    },
    {
      name: "Security Agent",
      key: "security" as const,
      description:
        "Checks vulnerabilities, secrets and unsafe code.",
    },
  ];

  const renderIssue = (
    issue: ReviewIssue,
    index: number
  ) => {
    return (
      <div className="agent-issue" key={index}>

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

      {/* HEADER */}

      <header className="header">

        <h1>
          CodeSentinel 🤖
        </h1>

        <p>
          AI-Powered GitHub Pull Request Code Review
        </p>

      </header>


      <main className="container">

        {/* REVIEW FORM */}

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


        {/* ERROR */}

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}


        {/* LOADING */}

        {loading && (
          <div className="loading">
            🤖 CodeSentinel is analyzing the Pull Request...
          </div>
        )}


        {/* RESULTS */}

        {result && (
          <section className="results">

            {/* AI PIPELINE */}

            <div className="agent-pipeline">

              <h2>
                AI Review Pipeline
              </h2>

              <div className="agents">

                {agents.map((agent) => (

                  <div
                    className="agent"
                    key={agent.key}
                  >

                    <div className="agent-check">
                      ✓
                    </div>

                    <strong>
                      {agent.name}
                    </strong>

                    <p>
                      {agent.description}
                    </p>

                  </div>

                ))}

                <div className="agent review-agent">

                  <div className="agent-check">
                    ✓
                  </div>

                  <strong>
                    Review Agent
                  </strong>

                  <p>
                    Combines all findings into the final review.
                  </p>

                </div>

              </div>

            </div>


            {/* SPECIALIST AGENTS */}

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


            {/* FINAL REVIEW */}

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


            {/* GITHUB */}

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