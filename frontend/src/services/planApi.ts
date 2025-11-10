import type { Message } from "../types/message";

export type PostPlanResult = { status: "ok"; data: Message } | { status: "auth"; authUrl: string };

export async function postPlan(date: string): Promise<PostPlanResult> {
  const res = await fetch("/api/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ date }),
  });

  if (res.status === 401) {
    const { auth_url } = await res.json();
    return { status: "auth", authUrl: auth_url };
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const data: Message = await res.json();
  return { status: "ok", data };
}