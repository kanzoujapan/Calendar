export function StatusBar({ count }: { count: number }) {
  return (
    <div className="flex items-center justify-between text-gray-500 text-sm font-mono px-4">
      <span className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></div>
        SYSTEM ACTIVE
      </span>
      <span>{count} ENTRIES</span>
    </div>
  );
}