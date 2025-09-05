import React, { useState } from 'react';

function UrlShortener() {
  const [originalUrl, setOriginalUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!originalUrl.trim()) {
      setError('Please enter a URL');
      return;
    }

    setLoading(true);
    setError('');
    setShortUrl('');

    try {
      const response = await fetch('http://localhost:8080/url-shortener/api/v1/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          original_url: originalUrl.trim(),
          url_type: 'RANDOM'
        }),
      });

      console.log(response);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to shorten URL');
      }

      const data = await response.json();
      setShortUrl(data.short_url);
    } catch (err) {
      setError(err.message || 'An error occurred while shortening the URL');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shortUrl);
    alert('Short URL copied to clipboard!');
  };

  return (
    <div className="container">
      <h1>URL Shortener</h1>
      <p className="subtitle">Shorten your long URLs quickly and easily</p>
      
      <form onSubmit={handleSubmit} className="url-form">
        <div className="input-group">
          <label htmlFor="originalUrl">Enter your long URL:</label>
          <input
            type="url"
            id="originalUrl"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
            placeholder="https://example.com/very/long/url/here"
            className="url-input"
            disabled={loading}
          />
        </div>
        
        <button 
          type="submit" 
          className="shorten-btn"
          disabled={loading}
        >
          {loading ? 'Shortening...' : 'Shorten URL'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {shortUrl && (
        <div className="result-section">
          <h3>Your Short URL:</h3>
          <div className="short-url-container">
            <input
              type="text"
              value={shortUrl}
              readOnly
              className="short-url-input"
            />
            <button 
              onClick={copyToClipboard}
              className="copy-btn"
            >
              Copy
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default UrlShortener; 