import { useEffect, useState } from "react";

export function useAuth() {
  const [isSignedIn, setIsSignedIn] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const signedIn = params.get("isSignedIn") === "true";
    if (signedIn) {
      setIsSignedIn(true);
      const newUrl = window.location.origin + window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }
  }, []);

  const redirectToAuth = () => {
    window.location.assign("/api/auth");
  };

  return { isSignedIn, redirectToAuth };
}