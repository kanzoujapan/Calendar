// main page 

import { BackgroundEffects, Header, MessageList, DatePickerForm, StatusBar, AuthSection, ErrorBanner } from "../components/index";
import { useAuth, usePlanMessages } from "../hooks/index";

export default function CheckTheDay() {
  const { isSignedIn, redirectToAuth } = useAuth();
  const { messages, sendDate, sending, error, clearError } = usePlanMessages();

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-8 relative overflow-hidden">
      <BackgroundEffects />
      <div className="w-full max-w-2xl relative z-10">
        <Header />

        <div className="bg-gray-900/80 backdrop-blur-xl rounded-2xl shadow-2xl border border-cyan-500/30 p-8 mb-6">
          {error && <ErrorBanner message={error} onClose={clearError} />}
          <MessageList messages={messages} />
          <DatePickerForm onSubmit={sendDate} sending={sending} />
          <AuthSection isSignedIn={isSignedIn} onSignIn={redirectToAuth} />
        </div>

        <StatusBar count={messages.length} />
      </div>
    </div>
  );
}