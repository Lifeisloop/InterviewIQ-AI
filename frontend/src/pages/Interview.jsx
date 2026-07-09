import { useState } from "react";
import {
  useLocation,
  useNavigate,
} from "react-router-dom";

import api from "../api/api";
import "../styles/interview.css";


function Interview() {
  const location = useLocation();
  const navigate = useNavigate();

  const resumeId = location.state?.resumeId;

  const [jobDescription, setJobDescription] =
    useState("");

  const [interviewId, setInterviewId] =
    useState(null);

  const [questions, setQuestions] =
    useState([]);

  const [answers, setAnswers] =
    useState([]);

  const [currentIndex, setCurrentIndex] =
    useState(0);

  const [loading, setLoading] =
    useState(false);

  const [submitting, setSubmitting] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [finalReport, setFinalReport] =
    useState(null);


  const handleStartInterview = async (e) => {
    e.preventDefault();

    if (!resumeId) {
      setMessage(
        "Resume ID not found. Please upload your resume again."
      );
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const response = await api.post(
        "/interview/start",
        {
          resume_id: resumeId,
          job_description: jobDescription,
        }
      );

      const data = response.data;
      const formattedQuestions = [];

      Object.entries(data.questions).forEach(
        ([category, categoryQuestions]) => {
          categoryQuestions.forEach(
            (question) => {
              formattedQuestions.push({
                category,
                question,
              });
            }
          );
        }
      );

      setInterviewId(data.interview_id);
      setQuestions(formattedQuestions);

      setAnswers(
        new Array(
          formattedQuestions.length
        ).fill("")
      );

      setCurrentIndex(0);

    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
        "Failed to start interview."
      );

    } finally {
      setLoading(false);
    }
  };


  const handleAnswerChange = (value) => {
    const updatedAnswers = [...answers];

    updatedAnswers[currentIndex] = value;

    setAnswers(updatedAnswers);
  };


  const handleSubmitInterview = async () => {
    const formattedAnswers = questions
      .map((item, index) => ({
        question: item.question,
        answer: answers[index].trim(),
      }))
      .filter(
        (item) => item.answer !== ""
      );

    if (formattedAnswers.length === 0) {
      setMessage(
        "Please answer at least one question."
      );
      return;
    }

    const unansweredCount =
      questions.length -
      formattedAnswers.length;

    if (unansweredCount > 0) {
      const shouldSubmit = window.confirm(
        `You have ${unansweredCount} unanswered questions. Submit answered questions only?`
      );

      if (!shouldSubmit) {
        return;
      }
    }

    try {
      setSubmitting(true);
      setMessage("");

      const response = await api.post(
        "/report/final",
        {
          interview_id: interviewId,
          answers: formattedAnswers,
        }
      );

      setFinalReport(response.data);

    } catch (error) {
      setMessage(
        error.response?.data?.detail ||
        "Failed to generate final report."
      );

    } finally {
      setSubmitting(false);
    }
  };


  const progressPercentage =
    questions.length > 0
      ? ((currentIndex + 1) /
          questions.length) *
        100
      : 0;


  if (finalReport) {
    return (
      <div className="interview-page">
        <div className="interview-container">

          <header className="interview-header">
            <div className="interview-brand">
              <div className="interview-logo">
                IQ
              </div>

              <div>
                <h1>InterviewIQ AI</h1>
                <p>Performance Report</p>
              </div>
            </div>

            <button
              className="back-button"
              onClick={() =>
                navigate("/dashboard")
              }
            >
              Back to Dashboard
            </button>
          </header>


          <main className="interview-card">
            <h1 className="interview-title">
              Final Interview Report
            </h1>

            <p className="interview-subtitle">
              AI-generated feedback based on
              your submitted interview answers.
            </p>


            <div className="report-score-card">
              <div className="report-score">
                {finalReport.average_score}/10
              </div>

              <div className="report-score-label">
                Overall Score ·{" "}
                {finalReport.total_questions}{" "}
                questions evaluated
              </div>
            </div>


            <div className="report-grid">

              <section className="report-panel">
                <h3>Strengths</h3>

                <ul>
                  {finalReport.strengths?.length
                    ? finalReport.strengths.map(
                        (item, index) => (
                          <li key={index}>
                            {item}
                          </li>
                        )
                      )
                    : (
                      <li>
                        No specific strengths detected.
                      </li>
                    )}
                </ul>
              </section>


              <section className="report-panel">
                <h3>Areas to Improve</h3>

                <ul>
                  {finalReport.weaknesses?.length
                    ? finalReport.weaknesses.map(
                        (item, index) => (
                          <li key={index}>
                            {item}
                          </li>
                        )
                      )
                    : (
                      <li>
                        No major weaknesses detected.
                      </li>
                    )}
                </ul>
              </section>

            </div>


            <section className="evaluation-section">
              <h2>Detailed Evaluations</h2>

              {finalReport.evaluations?.map(
                (evaluation, index) => (
                  <article
                    className="evaluation-card"
                    key={index}
                  >
                    <h3>
                      Question {index + 1}
                    </h3>

                    <p>
                      <strong>Question:</strong>{" "}
                      {evaluation.question}
                    </p>

                    <p>
                      <strong>Your Answer:</strong>{" "}
                      {evaluation.answer}
                    </p>

                    <div className="evaluation-score">
                      Score: {evaluation.score}/10
                    </div>

                    <div className="ideal-answer">
                      <strong>Ideal Answer</strong>

                      <p>
                        {evaluation.ideal_answer}
                      </p>
                    </div>
                  </article>
                )
              )}
            </section>
          </main>

        </div>
      </div>
    );
  }


  return (
    <div className="interview-page">
      <div className="interview-container">

        <header className="interview-header">
          <div className="interview-brand">
            <div className="interview-logo">
              IQ
            </div>

            <div>
              <h1>InterviewIQ AI</h1>
              <p>Personalized AI Interview</p>
            </div>
          </div>

          <button
            className="back-button"
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Back to Dashboard
          </button>
        </header>


        <main className="interview-card">

          {questions.length === 0 ? (
            <>
              <span className="resume-badge">
                Resume ID: {resumeId || "Missing"}
              </span>

              <h1 className="interview-title">
                Start Your AI Interview
              </h1>

              <p className="interview-subtitle">
                Paste the target job description.
                InterviewIQ will generate questions
                based on your resume and role.
              </p>


              <form onSubmit={handleStartInterview}>
                <textarea
                  className="job-textarea"
                  placeholder="Paste job description here..."
                  value={jobDescription}
                  onChange={(e) =>
                    setJobDescription(
                      e.target.value
                    )
                  }
                  required
                />

                <button
                  className="action-button"
                  type="submit"
                  disabled={loading}
                >
                  {loading
                    ? "Generating Questions..."
                    : "Generate AI Interview"}
                </button>
              </form>
            </>

          ) : (
            <>
              <div className="progress-header">
                <span>
                  Question {currentIndex + 1}{" "}
                  of {questions.length}
                </span>

                <span>
                  {Math.round(
                    progressPercentage
                  )}%
                </span>
              </div>


              <div className="progress-track">
                <div
                  className="progress-fill"
                  style={{
                    width:
                      `${progressPercentage}%`,
                  }}
                />
              </div>


              <span className="category-badge">
                {
                  questions[currentIndex]
                    .category
                }
              </span>


              <h2 className="question-text">
                {
                  questions[currentIndex]
                    .question
                }
              </h2>


              <textarea
                className="answer-textarea"
                placeholder="Type your answer here..."
                value={answers[currentIndex]}
                onChange={(e) =>
                  handleAnswerChange(
                    e.target.value
                  )
                }
              />


              <div className="interview-controls">

                <button
                  className="secondary-button"
                  onClick={() =>
                    setCurrentIndex(
                      currentIndex - 1
                    )
                  }
                  disabled={
                    currentIndex === 0
                  }
                >
                  Previous
                </button>


                {currentIndex <
                questions.length - 1 ? (

                  <button
                    className="next-button"
                    onClick={() =>
                      setCurrentIndex(
                        currentIndex + 1
                      )
                    }
                  >
                    Next Question
                  </button>

                ) : (

                  <button
                    className="submit-button"
                    onClick={
                      handleSubmitInterview
                    }
                    disabled={submitting}
                  >
                    {submitting
                      ? "Generating Report..."
                      : "Submit Interview"}
                  </button>

                )}

              </div>
            </>
          )}


          {message && (
            <div className="interview-message">
              {message}
            </div>
          )}

        </main>

      </div>
    </div>
  );
}


export default Interview;