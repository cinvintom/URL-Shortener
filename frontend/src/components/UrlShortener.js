import React, { useState } from 'react';

function UrlShortener() {
  const [originalUrl, setOriginalUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isShortUrlExists, setIsShortUrlExists] = useState(false);
  const [createdAt, setCreatedAt] = useState('');

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
      const response = await fetch(process.env.REACT_APP_API_URL + '/generate', {
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
      setIsShortUrlExists(data.is_short_url_exists);
      setCreatedAt(data.created_at);
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

  const redirectToShortUrl = () => {
    window.open(shortUrl, '_blank');
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
              onClick={redirectToShortUrl}
              style={{ cursor: 'pointer' }}
              title="Click to redirect"
              onMouseOver={e => {
                e.target.setAttribute('title', 'Click to redirect');
                e.target.style.backgroundColor = '#e0f7fa';
              }}
              onMouseOut={e => {
                e.target.style.backgroundColor = 'transparent';
              }}
            />
            <button
              onClick={copyToClipboard}
              className="copy-btn"
              type="button"
            >
              Copy
            </button>
          </div>
          {isShortUrlExists && (
            <div
              className="info-message"
              style={{
                marginTop: '8px',
                color: '#888',
                fontSize: '0.95em'
              }}
            >
              Already generated short URL on {createdAt ? new Date(createdAt + 'Z').toLocaleString() : ''}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default UrlShortener; 