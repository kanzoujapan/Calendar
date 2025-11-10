import { useState } from "react";
import type { Message } from "../types/message";
import { postPlan } from "../services/planApi";

export function usePlanMessages() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendDate = async (date: string) => {
    if (!date || sending) return;
    setSending(true);
    setError(null);
    try {
      const result = await postPlan(date);
      if (result.status === "auth") {
        window.location.href = result.authUrl;
        return;
      }
      setMessages((prev) => [...prev, result.data]); // 競合回避の関数形式
    } catch (e: any) {
      setError(e?.message ?? "送信に失敗しました");
    } finally {
      setSending(false);
    }
  };

  return { messages, sendDate, sending, error, clearError: () => setError(null) };
}