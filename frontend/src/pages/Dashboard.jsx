import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";
import "../styles/dashboard.css";


function Dashboard() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(false);


  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a PDF resume.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const formData = new FormData();

      formData.append(
        "file",
        file
      );

      const response = await api.post(
        "/resume/upload-resume",
        formData
      );

      console.log(
        "FULL RESUME RESPONSE:",
        response.data
      );

      setResumeData(response.data);

      setMessage(
        "Resume analyzed successfully."
      );

    } catch (error) {
      console.error(
        "UPLOAD ERROR:",
        error.response?.data
      );

      setMessage(
        error.response?.data?.detail ||
        error.response?.data?.message ||
        "Resume upload failed."
      );

    } finally {
      setLoading(false);
    }
  };


  const handleLogout = () => {
    localStorage.removeItem(
      "access_token"
    );

    navigate("/");
  };


  const handleStartInterview = () => {
    if (!resumeData?.resume_id) {
      setMessage(
        "Resume ID not found. Please upload your resume again."
      );

      return;
    }

    navigate(
      "/interview",
      {
        state: {
          resumeId:
            resumeData.resume_id,
        },
      }
    );
  };


  return (
    <div className="dashboard-page">

      <div className="dashboard-container">

        <header className="dashboard-header">

          <div className="dashboard-brand">

            <div className="dashboard-logo">
              IQ
            </div>

            <div>
              <h1>InterviewIQ AI</h1>

              <p>
                AI Interview Preparation Platform
              </p>
            </div>

          </div>


          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>

        </header>


        <section className="dashboard-hero">

          <h2>
            Prepare smarter for your
            next interview.
          </h2>

          <p>
            Upload your resume, let InterviewIQ
            identify your skills, and generate a
            personalized AI interview based on your
            profile and target job description.
          </p>

        </section>


        <main className="dashboard-grid">

          <section className="dashboard-card">

            <h2 className="card-heading">
              Upload Resume
            </h2>

            <p className="card-description">
              Upload a PDF resume to extract your
              profile and technical skills.
            </p>


            <form onSubmit={handleUpload}>

              <div className="upload-zone">

                <div className="upload-icon">
                  ↑
                </div>

                <h3>
                  Select your resume
                </h3>

                <p className="card-description">
                  PDF files only
                </p>


                <input
                  className="file-input"
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(e) => {
                    const selectedFile =
                      e.target.files?.[0];

                    setFile(
                      selectedFile || null
                    );

                    setMessage("");
                  }}
                />


                {file && (
                  <p className="file-name">
                    Selected: {file.name}
                  </p>
                )}

              </div>


              <button
                className="upload-button"
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Analyzing Resume..."
                  : "Analyze Resume"}
              </button>

            </form>


            {message && (
              <div className="dashboard-message">
                {message}
              </div>
            )}

          </section>


          <section className="dashboard-card">

            <h2 className="card-heading">
              Candidate Profile
            </h2>

            <p className="card-description">
              Extracted information from your
              latest uploaded resume.
            </p>


            {!resumeData ? (

              <div className="profile-placeholder">
                Upload and analyze your resume
                to view candidate information
                and detected skills.
              </div>

            ) : (

              <>
                <div className="profile-list">

                  <div className="profile-item">
                    <span className="profile-label">
                      Name
                    </span>

                    <span className="profile-value">
                      {resumeData.candidate_name ||
                        "Not detected"}
                    </span>
                  </div>


                  <div className="profile-item">
                    <span className="profile-label">
                      Email
                    </span>

                    <span className="profile-value">
                      {resumeData.candidate_email ||
                        "Not detected"}
                    </span>
                  </div>


                  <div className="profile-item">
                    <span className="profile-label">
                      Phone
                    </span>

                    <span className="profile-value">
                      {resumeData.candidate_phone ||
                        "Not detected"}
                    </span>
                  </div>


                  <div className="profile-item">
                    <span className="profile-label">
                      Resume ID
                    </span>

                    <span className="profile-value">
                      {resumeData.resume_id}
                    </span>
                  </div>

                </div>


                <div className="skills-section">

                  <h3>
                    Detected Skills
                  </h3>


                  <div className="skills-list">

                    {resumeData.skills?.length > 0 ? (

                      resumeData.skills.map(
                        (skill, index) => (
                          <span
                            className="skill-chip"
                            key={`${skill}-${index}`}
                          >
                            {skill}
                          </span>
                        )
                      )

                    ) : (

                      <span className="profile-value">
                        No skills detected
                      </span>

                    )}

                  </div>

                </div>


                <button
                  className="start-interview-button"
                  onClick={handleStartInterview}
                >
                  Start AI Interview
                </button>

              </>

            )}

          </section>

        </main>

      </div>

    </div>
  );
}


export default Dashboard;