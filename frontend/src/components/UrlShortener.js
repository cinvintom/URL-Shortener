import React, { useState, useRef } from 'react';

function UrlShortener() {
  const [originalUrl, setOriginalUrl] = useState('');
  const [shortUrl, setShortUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isShortUrlExists, setIsShortUrlExists] = useState(false);
  const [updatedAt, setUpdatedAt] = useState('');

  // Custom URL states
  const [useCustomUrl, setUseCustomUrl] = useState(false);
  const [customUrl, setCustomUrl] = useState('');
  const [customUrlError, setCustomUrlError] = useState('');
  const [customUrlAvailable, setCustomUrlAvailable] = useState(null);
  const customUrlTimeoutRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!originalUrl.trim()) {
      setError('Please enter a URL');
      return;
    }

    if (useCustomUrl) {
      if (!customUrl) {
        setError('Please enter a custom short URL');
        return;
      }
      if (customUrlError || customUrlAvailable === false) {
        setError('Custom short URL is not available');
        return;
      }
    }

    setLoading(true);
    setError('');
    setShortUrl('');

    try {
      const payload = {
        original_url: originalUrl.trim(),
        url_type: useCustomUrl ? 'CUSTOM' : 'RANDOM',
      };
      if (useCustomUrl) {
        payload['short_url'] = customUrl;
      }

      const response = await fetch(
        (process.env.REACT_APP_API_URL || '/api/v1') + '/generate',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to shorten URL');
      }

      const data = await response.json();
      setShortUrl(data.short_url);
      setIsShortUrlExists(data.is_short_url_exists);
      setUpdatedAt(data.updated_at);
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

  const newShortUrl = () => {
    if (shortUrl) {
      clearForm();
    }
  };

  const clearForm = () => {
    setShortUrl('');
    setIsShortUrlExists(false);
    setUpdatedAt('');
    setUseCustomUrl(false);
    setCustomUrl('');
    setCustomUrlError('');
    setCustomUrlAvailable(null);
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
            onClick={() => newShortUrl()}
          />
        </div>

        <button
          type="submit"
          className="shorten-btn"
          disabled={loading}
          onClick={() => { newShortUrl(); }}
        >
          {loading ? 'Shortening...' : 'Shorten URL'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* Custom Short URL Feature */}
      {!shortUrl && <div className="custom-url-section" style={{ marginTop: '18px' }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <input
            type="checkbox"
            checked={useCustomUrl}
            onChange={(e) => {
              setUseCustomUrl(e.target.checked);
              setCustomUrl('');
              setCustomUrlError('');
              setCustomUrlAvailable(null);
            }}
            disabled={loading}
          />
          Create custom short URL
        </label>
        {useCustomUrl && (
          <div className="input-group" style={{ marginTop: '10px' }}>
            <label htmlFor="customUrl">Custom short URL:</label>
            <input
              type="text"
              id="customUrl"
              value={customUrl}
              onChange={async (e) => {
                const value = e.target.value;
                // Only allow alphanumeric, max 10 chars
                const sanitized = value.replace(/[^a-zA-Z0-9]/g, '').slice(0, 10);
                setCustomUrl(sanitized);

                if (sanitized.length === 0) {
                  setCustomUrlError('');
                  setCustomUrlAvailable(null);
                  return;
                }
                if (sanitized.length > 10) {
                  setCustomUrlError('Maximum 10 characters allowed');
                  setCustomUrlAvailable(null);
                  return;
                }
                setCustomUrlError('');
                setCustomUrlAvailable(null);

                // Debounce API call for availability
                if (customUrlTimeoutRef.current) {
                  clearTimeout(customUrlTimeoutRef.current);
                }
                customUrlTimeoutRef.current = setTimeout(async () => {
                  try {
                    const resp = await fetch(
                      (process.env.REACT_APP_API_URL || '/api/v1') +
                        `/custom_url/available/${encodeURIComponent(sanitized)}`
                    );
                    if (!resp.ok) {
                      setCustomUrlError('Error checking custom URL availability');
                      setCustomUrlAvailable(null);
                      return;
                    }
                    const data = await resp.json();
                    if (!data.is_short_url_available) {
                      setCustomUrlError('Custom URL exists, please change');
                      setCustomUrlAvailable(false);
                    } else {
                      setCustomUrlError('');
                      setCustomUrlAvailable(true);
                    }
                  } catch (err) {
                    setCustomUrlError('Error checking custom URL availability');
                    setCustomUrlAvailable(null);
                  }
                }, 400);
              }}
              placeholder="Alphabets and numbers, max 10"
              className="url-input"
              disabled={loading}
              maxLength={10}
              autoComplete="off"
              style={{
                borderColor:
                  customUrlError
                    ? '#e57373'
                    : customUrlAvailable === true
                    ? '#81c784'
                    : undefined,
              }}
            />
            {customUrlError && (
              <div className="error-message" style={{ marginTop: '4px' }}>
                {customUrlError}
              </div>
            )}
            {customUrlAvailable && !customUrlError && (
              <div
                className="info-message"
                style={{
                  marginTop: '4px',
                  color: '#388e3c',
                  fontSize: '0.95em',
                }}
              >
                Custom URL is available!
              </div>
            )}
          </div>
        )}
      </div>}

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
              {isShortUrlExists && customUrl ?
                `Updated short URL with custom URL ` :
                `Already generated short URL available`}
              <div
                style={{
                  marginTop: '4px',
                  color: '#888',
                  fontSize: '0.6em',
                  fontStyle: 'italic'
                }}
              >
                Last updated at {updatedAt ? new Date(updatedAt + 'Z').toLocaleString() : ''}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default UrlShortener;