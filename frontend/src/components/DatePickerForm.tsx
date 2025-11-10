import { useState } from "react";
import { Send } from "lucide-react";

export function DatePickerForm({
  onSubmit,
  sending,
}: {
  onSubmit: (date: string) => void;
  sending?: boolean;
}) {
  const [date, setDate] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(date);
    if (!sending) setDate("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <div className="flex-1 relative">
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="w-full px-6 py-4 bg-gray-800 border-2 border-cyan-500/50 rounded-xl text-cyan-100 focus:outline-none focus:border-cyan-400 focus:shadow-lg focus:shadow-cyan-500/20 transition-all text-lg font-mono"
          style={{ colorScheme: "dark" }}
        />
      </div>
      <button
        type="submit"
        disabled={sending}
        className="px-8 py-4 bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 rounded-xl transition-all flex items-center gap-2 text-white font-bold shadow-lg shadow-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/50 group border border-cyan-400/30 disabled:opacity-50"
      >
        <Send className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        {sending ? "SENDING..." : "SEND"}
      </button>
    </form>
  );
}