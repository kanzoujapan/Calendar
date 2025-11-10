export function ErrorBanner({
  message,
  onClose,
}: {
  message: string;
  onClose: () => void;
}) {
  return (
    <div className="mb-4 rounded-lg border border-red-500/40 bg-red-900/30 text-red-200 px-4 py-3 flex justify-between">
      <span className="font-mono">{message}</span>
      <button onClick={onClose} className="underline">close</button>
    </div>
  );
}