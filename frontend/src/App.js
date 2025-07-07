import React, { useState, useEffect } from 'react';
import ChatBox from './components/ChatBox';
import './App.css';

function App() {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [ollamaStatus, setOllamaStatus] = useState('checking');

  // Ollama 모델 목록 및 상태 확인 API 호출 (예시)
  useEffect(() => {
    async function fetchModelsAndStatus() {
      try {
        // 실제 ollama API 엔드포인트에 맞게 수정 필요
        const res = await fetch('http://localhost:11434/api/tags');
        if (!res.ok) throw new Error('Ollama not running');
        const data = await res.json();
        setModels(data.models || []);
        setSelectedModel(data.models?.[0]?.name || '');
        setOllamaStatus('connected');
      } catch {
        setModels([]);
        setSelectedModel('');
        setOllamaStatus('disconnected');
      }
    }
    fetchModelsAndStatus();
  }, []);

  // ChatBox에 모델 정보와 상태 전달
  const handleChatSend = async (msg) => {
    if (ollamaStatus !== 'connected') {
      throw new Error('LLM 모델과 연결이 필요합니다');
    }
    // 실제 ollama inference API 연동 필요
    return '';
  };

  return (
    <div className="App" style={{ paddingBottom: 260 }}>
      <div style={{
        width: '100%', maxWidth: 680, margin: '0 auto', padding: '24px 0 8px 0',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div>
          <select
            value={selectedModel}
            onChange={e => setSelectedModel(e.target.value)}
            disabled={ollamaStatus !== 'connected'}
            style={{ padding: '8px', borderRadius: 8, fontSize: 16 }}
          >
            {models.map(m => (
              <option key={m.name} value={m.name}>{m.name}</option>
            ))}
          </select>
        </div>
        <div style={{ color: ollamaStatus === 'connected' ? '#61dafb' : '#ff5252', fontWeight: 600 }}>
          {ollamaStatus === 'connected' ? 'Ollama 연결됨' : 'Ollama 실행 필요'}
        </div>
      </div>
      <ChatBox onSend={handleChatSend} ollamaStatus={ollamaStatus} />
    </div>
  );
}

export default App;
