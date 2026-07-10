import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";
import "../styles/auth.css";


function Register() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setMessage("");

      await api.post(
        "/auth/register",
        {
          full_name: fullName,
          email,
          password,
        }
      );

      navigate("/");

    } catch (error) {
      const detail = error.response?.data?.detail;
      let errMsg = "Registration failed.";
      if (typeof detail === "string") {
        errMsg = detail;
      } else if (Array.isArray(detail)) {
        errMsg = detail.map(err => err.msg).join(", ");
      }
      setMessage(errMsg);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="auth-page">

      <div className="auth-card">

        <div className="auth-brand">
          <div className="auth-logo">
            IQ
          </div>

          <h1>Create Account</h1>

          <p>
            Start practicing personalized
            AI-powered interviews.
          </p>
        </div>


        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >

          <div className="form-group">
            <label>Full Name</label>

            <input
              type="text"
              placeholder="Enter your full name"
              value={fullName}
              onChange={(e) =>
                setFullName(e.target.value)
              }
              required
            />
          </div>


          <div className="form-group">
            <label>Email Address</label>

            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) =>
                setEmail(e.target.value)
              }
              required
            />
          </div>


          <div className="form-group">
            <label>Password</label>

            <input
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              required
            />
          </div>


          <button
            className="primary-button"
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Creating account..."
              : "Create Account"}
          </button>

        </form>


        {message && (
          <p className="auth-message">
            {message}
          </p>
        )}


        <div className="auth-footer">
          Already have an account?

          <button
            className="auth-link"
            onClick={() =>
              navigate("/")
            }
          >
            Sign in
          </button>
        </div>

      </div>

    </div>
  );
}


export default Register;