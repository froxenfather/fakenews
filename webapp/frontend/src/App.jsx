// please dont touch this file, its the frontend react code for the website, and I used a react builder to make it look nice, so I dont fully understand how it works.
//  all styling is in the index.css file, so if you want to change the look of the website, thats where you should do it. 
// The only thing I really want to change in this file is the handleSubmit function, which is where we will call the backend API and get the prediction result.
//  The rest of this is just boilerplate for setting up the frontend and handling user input, so I would prefer if we just left it alone unless we need to change something specific.

import { useState } from "react";
import "./index.css";

function looksLikeWebsite(value) {
  const trimmed = value.trim();
  if (!trimmed) return false;

  try {
    const withProtocol = /^https?:\/\//i.test(trimmed)
      ? trimmed
      : `https://${trimmed}`;

    const url = new URL(withProtocol);

    return (
      !!url.hostname &&
      url.hostname.includes(".") &&
      !url.hostname.startsWith(".") &&
      !url.hostname.endsWith(".")
    );
  } catch {
    return false;
  }
}

function youFuckedUp(err) {
  if (!err) return "Something broke. Oops.";

  if (typeof err === "string") {
    if (
      err.toLowerCase().includes("failed to fetch") ||
      err.toLowerCase().includes("networkerror")
    ) {
      return "Can't reach the backend right now.";
    }
    return err;
  }

  if (typeof err === "object") {
    if (typeof err.detail === "string") return err.detail;
    if (typeof err.message === "string") return err.message;
  }

  return "something went wrong.";
}

export default function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    const trimmed = url.trim();

    if (!looksLikeWebsite(trimmed)) {
      setError("That's not a website bro");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something broke");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  // Mess with this to mess with website
  return (
    <div className="page">
      <div className="hero">
        <h1 className="title">The Fake News Detector</h1>
        <p className="subtitle">
          Paste a news article link and let us do our thing.
        </p>

        
        {/*please tell me this is a comment */}
        {/*Okay, This messes with the transcludent textbox */}
        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            placeholder="Paste a URL here..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            className="urlInput"
          />
          {/*Button to analyze the URL */}
          <button type="submit" disabled={loading} className="analyzeButton">
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </form>
        {/* Preloaded React stuff, Dont touch, Dont know what it does*/}
        {error && <div className="errorMessage">{error}</div>}
        {/* Result panel */}
        {result && (
          <div className="resultPanel">
            <h2>Result</h2>
            <p><strong>URL:</strong> {result.url}</p>
            <p><strong>Status:</strong> {result.scrape_status}</p>
            <p><strong>Word Count:</strong> {result.scraped_word_count}</p>
            <p><strong>Prediction:</strong> {result.prediction.label}</p>
            <p><strong>Confidence:</strong> {result.prediction.confidence}</p>

            <details>
              <summary>Preview scraped text</summary>
              <p>{result.preview}</p>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}