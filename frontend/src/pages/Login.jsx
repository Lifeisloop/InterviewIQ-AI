import { useEffect,useState, } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";
import "../styles/auth.css";


function Login() {
  const navigate = useNavigate();

  useEffect(() => {
  const token = localStorage.getItem(
    "access_token"
  );

  if (token) {
    navigate(
      "/dashboard",
      { replace: true }
    );
  }
}, [navigate]);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);


  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password.length < 8) {
      alert("Password must be at least 8 characters long.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      const response = await api.post(
        "/auth/login",
        {
          email,
          password,
        }
      );

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      navigate("/dashboard");

    } catch (error) {
      const detail = error.response?.data?.detail;
      let errMsg = "Login failed. Please check your credentials.";
      if (typeof detail === "string") {
        errMsg = detail;
      } else if (Array.isArray(detail)) {
        errMsg = detail.map(err => err.msg).join(", ");
      }
      setMessage(errMsg);
      alert(errMsg);
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

          <h1>InterviewIQ AI</h1>

          <p>
            Practice smarter interviews with
            AI-powered personalized feedback.
          </p>
        </div>


        <form
          className="auth-form"
          onSubmit={handleSubmit}
        >

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
              placeholder="Enter your password"
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
              ? "Signing in..."
              : "Sign In"}
          </button>

        </form>


        {message && (
          <p className="auth-message">
            {message}
          </p>
        )}


        <div className="auth-footer">
          Don't have an account?

          <button
            className="auth-link"
            onClick={() =>
              navigate("/register")
            }
          >
            Create account
          </button>
        </div>

      </div>

    </div>
  );
}


export default Login;