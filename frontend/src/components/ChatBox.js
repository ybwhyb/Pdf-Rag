import React, { useState, useRef, useEffect } from 'react';
import './ChatBox.css';
import { FaPlus, FaMicrophone } from 'react-icons/fa';
import { uploadFile } from '../api';

function ChatBox({ onSend, ollamaStatus }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadMessage, setUploadMessage] = useState("");
  const fileInputRef = useRef(null);
  const allowedExtensions = ['.pdf', '.hwp'];
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { from: 'user', text: input }]);
    setInput("");
    setLoading(true);
    setErrorMessage("");
    if (onSend) {
      try {
        const reply = await onSend(input);
        if (reply) {
          setMessages(msgs => [...msgs, { from: 'bot', text: reply }]);
        }
      } catch (e) {
        setErrorMessage(e.message || 'LLM 모델과 연결이 필요합니다');
      }
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handlePlusClick = () => {
    if (!loading) fileInputRef.current.click();
  };

  const checkExtension = (filename) => {
    if (!filename) return false;
    return allowedExtensions.some(ext => filename.toLowerCase().endsWith(ext));
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploadProgress(0);
    setUploadMessage("");
    if (!checkExtension(file.name)) {
      setUploadMessage("지원하지 않는 파일 형식입니다. (pdf, hwp만 가능)");
      return;
    }
    try {
      const res = await uploadFile(file, (event) => {
        if (event.total) {
          setUploadProgress(Math.round((event.loaded * 100) / event.total));
        }
      });
      setUploadMessage(`업로드 및 임베딩 성공: ${res.data.filename}`);
      setUploadProgress(100);
    } catch (err) {
      setUploadMessage("업로드 실패: " + (err.response?.data?.detail || err.message));
      setUploadProgress(0);
    }
  };

  return (
    <div className="gpt-chatbox-outer">
      <div className="gpt-chatbox-inner">
        <div className="gpt-chatbox-messages">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`gpt-chatbox-msg gpt-chatbox-msg-${msg.from}`}
            >
              {msg.text}
            </div>
          ))}
          {loading && (
            <div className="gpt-chatbox-msg gpt-chatbox-msg-bot gpt-chatbox-loading">
              <span className="chatbox-spinner"></span> 답변을 생성 중입니다...
            </div>
          )}
          {errorMessage && (
            <div className="gpt-chatbox-msg gpt-chatbox-msg-bot" style={{ color: '#ff5252', fontWeight: 600 }}>
              {errorMessage}
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="gpt-chatbox-input-area">
          <input
            type="file"
            accept=".pdf,.hwp"
            style={{ display: 'none' }}
            ref={fileInputRef}
            onChange={handleFileChange}
          />
          <button className="gpt-chatbox-icon-btn" type="button" disabled={loading} onClick={handlePlusClick}>
            <FaPlus />
          </button>
          <textarea
            className="gpt-chatbox-input"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="무엇이든 부탁하세요"
            disabled={loading}
            rows={1}
          />
          <button className="gpt-chatbox-icon-btn" type="button" disabled={loading} style={{marginRight: '8px'}}>
            <FaMicrophone />
          </button>
          <button className="gpt-chatbox-send" onClick={handleSend} disabled={loading || !input.trim()}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2 21L23 12L2 3V10L17 12L2 14V21Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
        {uploadProgress > 0 && (
          <div className="gpt-chatbox-upload-progress">
            <div className="gpt-chatbox-upload-bar" style={{ width: `${uploadProgress}%` }} />
            <span className="gpt-chatbox-upload-text">{uploadProgress}%</span>
          </div>
        )}
        {uploadMessage && (
          <div className="gpt-chatbox-upload-message">{uploadMessage}</div>
        )}
      </div>
    </div>
  );
}

export default ChatBox; 