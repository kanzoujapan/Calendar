import { Zap } from "lucide-react";

export function Header() {
  return (
    <div className="text-center mb-8">
      <div className="flex items-center justify-center gap-3 mb-4">
        <Zap className="w-8 h-8 text-cyan-400" />
        <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400">
          Check the Day
        </h1>
        <Zap className="w-8 h-8 text-purple-400" />
      </div>
      <p className="text-gray-400 text-lg">予定をチェック</p>
    </div>
  );
}