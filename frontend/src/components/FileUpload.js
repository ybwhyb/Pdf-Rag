import React, { useState } from 'react';
import { uploadFile } from '../api';
import './FileUpload.css';
import { FaPlus } from 'react-icons/fa';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [progress, setProgress] = useState(0);

  const allowedExtensions = ['.pdf', '.hwp'];

  const handleChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setMessage("");
    setProgress(0);
    if (selectedFile) {
      handleUpload(selectedFile);
    }
  };

  const checkExtension = (filename) => {
    if (!filename) return false;
    return allowedExtensions.some(ext => filename.toLowerCase().endsWith(ext));
  };

  const handleUpload = async (uploadFileObj) => {
    const uploadTarget = uploadFileObj || file;
    if (!uploadTarget) {
      setMessage("파일을 선택하세요.");
      return;
    }
    if (!checkExtension(uploadTarget.name)) {
      setMessage("지원하지 않는 파일 형식입니다. (pdf, hwp만 가능)");
      return;
    }
    setProgress(0);
    try {
      const res = await uploadFile(uploadTarget, (event) => {
        if (event.total) {
          setProgress(Math.round((event.loaded * 100) / event.total));
        }
      });
      setMessage(`업로드 및 임베딩 성공: ${res.data.filename}`);
      setProgress(100);
    } catch (err) {
      setMessage("업로드 실패: " + (err.response?.data?.detail || err.message));
      setProgress(0);
    }
  };

  return (
    <div className="fileupload-container">
      <label className="fileupload-label">
        <input type="file" onChange={handleChange} className="fileupload-input" />
        <span className="fileupload-plus-btn"><FaPlus size={24} /></span>
      </label>
      {progress > 0 && (
        <div className="fileupload-progress">
          <div className="fileupload-progress-bar" style={{ width: `${progress}%` }} />
          <span className="fileupload-progress-text">{progress}%</span>
        </div>
      )}
      <div className="fileupload-message">{message}</div>
    </div>
  );
}

export default FileUpload; 