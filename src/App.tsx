import React, { useState } from 'react';
import { Send, Calendar, Zap } from 'lucide-react';

export default function CheckTheDay() {
  const [selectedDate, setSelectedDate] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSubmit = () => {
    if (!selectedDate) return;
    
    const newMessage = {
      date: selectedDate,
      timestamp: new Date().toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' })
    };
    
    setMessages([...messages, newMessage]);
    setSelectedDate('');
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-8 relative overflow-hidden">
      {/* 背景エフェクト */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 via-transparent to-purple-500/10"></div>
      <div className="absolute top-20 left-20 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl"></div>
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"></div>

      <div className="w-full max-w-2xl relative z-10">
        {/* ヘッダー */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Zap className="w-8 h-8 text-cyan-400" />
            <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
              Check the Day
            </h1>
            <Zap className="w-8 h-8 text-purple-400" />
          </div>
          <p className="text-gray-400 text-lg">未来の日付をチェック</p>
        </div>

        {/* メインカード */}
        <div className="bg-gray-900/80 backdrop-blur-xl rounded-2xl shadow-2xl border border-cyan-500/30 p-8 mb-6">
          {/* メッセージエリア */}
          <div className="mb-6 h-64 overflow-y-auto space-y-3">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <p className="text-gray-500 text-center font-mono">
                  :: WAITING FOR INPUT ::<br />
                  <span className="text-cyan-400/50 text-sm">日付を選択してください</span>
                </p>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className="bg-gradient-to-r from-cyan-900/40 to-purple-900/40 rounded-xl p-4 border border-cyan-500/50 shadow-lg hover:border-cyan-400 transition-all">
                  <div className="flex items-center gap-3">
                    <Calendar className="w-5 h-5 text-cyan-400" />
                    <span className="text-cyan-100 font-bold text-lg font-mono">{msg.date}</span>
                    <span className="text-gray-400 text-sm ml-auto font-mono">{msg.timestamp}</span>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* 入力エリア */}
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                className="w-full px-6 py-4 bg-gray-800 border-2 border-cyan-500/50 rounded-xl text-cyan-100 focus:outline-none focus:border-cyan-400 focus:shadow-lg focus:shadow-cyan-500/20 transition-all text-lg font-mono"
                style={{ colorScheme: 'dark' }}
              />
            </div>
            <button
              onClick={handleSubmit}
              className="px-8 py-4 bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 rounded-xl transition-all flex items-center gap-2 text-white font-bold shadow-lg shadow-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/50 group border border-cyan-400/30"
            >
              <Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              SEND
            </button>
          </div>
        </div>

        {/* ステータスバー */}
        <div className="flex items-center justify-between text-gray-500 text-sm font-mono px-4">
          <span className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></div>
            SYSTEM ACTIVE
          </span>
          <span>{messages.length} ENTRIES</span>
        </div>
      </div>
    </div>
  );
}