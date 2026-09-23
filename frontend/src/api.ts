import type { DemoQuery, RunResult } from "./types";

const BASE = "/api";

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}

export const runQuery = (query: string) =>
  fetch(`${BASE}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  }).then((r) => json<RunResult>(r));

export const getRuns = () => fetch(`${BASE}/runs`).then((r) => json<RunResult[]>(r));

export const getExamples = () => fetch(`${BASE}/examples`).then((r) => json<DemoQuery[]>(r));
