export function AuthSection({
  isSignedIn,
  onSignIn,
}: {
  isSignedIn: boolean;
  onSignIn: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <p className="text-gray-400 mb-2">
        {isSignedIn ? "Signed in successfully!" : "You are not signed in."}
      </p>

      {isSignedIn ? (
        <button
          className="px-4 py-2 border rounded-lg text-red-300 hover:bg-red-800 transition"
          onClick={() => alert("You are already signed in!")}
        >
          Signed In
        </button>
      ) : (
        <button
          onClick={onSignIn}
          className="px-4 py-2 border rounded-lg text-cyan-300 hover:bg-cyan-800 transition"
        >
          Sign in
        </button>
      )}
    </div>
  );
}