import { Calendar } from "lucide-react";
import type { Message } from "../types/message";

export function MessageList({ messages }: { messages: Message[] }) {
  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 mb-6">
        <p className="text-gray-500 text-center font-mono">
          :: WAITING FOR INPUT ::<br />
          <span className="text-cyan-400/50 text-sm">日付を選択してください</span>
        </p>
      </div>
    );
  }

  return (
    <div className="mb-6 h-64 overflow-y-auto space-y-3">
      {messages.map((msg, idx) => (
        <div
          key={idx}
          className="bg-gradient-to-r from-cyan-900/40 to-purple-900/40 rounded-xl p-4 border border-cyan-500/50 shadow-lg hover:border-cyan-400 transition-all"
        >
          <div className="flex items-center gap-3">
            <Calendar className="w-5 h-5 text-cyan-400" />
            <span className="text-cyan-100 font-bold text-lg font-mono">{msg.date}</span>
            <span className="text-gray-400 text-sm ml-auto font-mono">{msg.timestamp}</span>
          </div>
        </div>
      ))}
    </div>
  );
}