import { useEffect, useMemo, useState } from "react";
import { GitBranch, Loader2, Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { StatTile } from "@/components/stat-tile";
import { GraphDiagram } from "@/components/graph-diagram";
import { StepTrace } from "@/components/step-trace";
import { useTheme } from "@/lib/use-theme";
import { getExamples, getRuns, runQuery } from "./api";
import type { DemoQuery, RunResult } from "./types";

function ThemeToggle() {
  const { theme, toggle } = useTheme();
  return (
    <Button variant="outline" size="icon" onClick={toggle} aria-label="Toggle theme">
      {theme === "dark" ? <Sun className="size-4" /> : <Moon className="size-4" />}
    </Button>
  );
}

export default function App() {
  const [examples, setExamples] = useState<DemoQuery[]>([]);
  const [runs, setRuns] = useState<RunResult[]>([]);
  const [result, setResult] = useState<RunResult | null>(null);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [provider, setProvider] = useState("mock");

  useEffect(() => {
    getExamples().then(setExamples).catch(() => {});
    getRuns().then(setRuns).catch(() => {});
    fetch("/api/health").then((r) => r.json()).then((d) => setProvider(d.provider)).catch(() => {});
  }, []);

  async function execute(q: string) {
    setLoading(true);
    setError(null);
    try {
      const res = await runQuery(q);
      setResult(res);
      setRuns((prev) => [res, ...prev].slice(0, 30));
    } catch (e) {
      setError(e instanceof Error ? e.message : "run failed");
    } finally {
      setLoading(false);
    }
  }

  const stats = useMemo(() => {
    const total = runs.length;
    const escalated = runs.filter((r) => r.escalation_reason).length;
    const avgSteps = total ? runs.reduce((s, r) => s + r.steps.length, 0) / total : 0;
    const avgLatency = total ? runs.reduce((s, r) => s + r.total_latency_ms, 0) / total : 0;
    return { total, escalated, avgSteps, avgLatency };
  }, [runs]);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2.5">
            <GitBranch className="size-6 text-primary" />
            <div>
              <h1 className="text-lg font-semibold leading-tight">JevLangGraph</h1>
              <p className="text-xs text-muted-foreground">A LangGraph agent where Jev, not an LLM, controls every branch point</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="rounded-full border px-2.5 py-1 font-mono text-xs text-muted-foreground">provider: {provider}</span>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl space-y-6 px-6 py-8">
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          <StatTile label="Runs" value={String(stats.total)} />
          <StatTile label="Escalated to human" value={String(stats.escalated)} />
          <StatTile label="Avg steps per run" value={stats.avgSteps.toFixed(1)} />
          <StatTile label="Avg total latency" value={`${stats.avgLatency.toFixed(1)} ms`} />
        </div>

        <div className="grid gap-6 lg:grid-cols-5">
          <div className="space-y-6 lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Try a demo query</CardTitle>
                <CardDescription>Each one exercises a different branch of the graph.</CardDescription>
              </CardHeader>
              <CardContent className="flex flex-col gap-2">
                {examples.map((ex, i) => (
                  <button
                    key={i}
                    onClick={() => execute(ex.query)}
                    disabled={loading}
                    className="rounded-md border bg-card px-3 py-2 text-left text-xs transition-colors hover:bg-accent hover:text-accent-foreground disabled:opacity-50"
                  >
                    <span className="text-muted-foreground">{ex.category}:</span> {ex.query}
                  </button>
                ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Or ask your own</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-1.5">
                  <Label htmlFor="query">Query</Label>
                  <Textarea id="query" rows={3} value={query} onChange={(e) => setQuery(e.target.value)} placeholder="e.g. What is 12 + 30?" />
                </div>
                <Button onClick={() => execute(query)} disabled={loading || !query.trim()} className="w-full">
                  {loading && <Loader2 className="size-4 animate-spin" />}
                  Run
                </Button>
                {error && <p className="text-sm text-critical">{error}</p>}
              </CardContent>
            </Card>
          </div>

          <div className="lg:col-span-3">
            {result ? (
              <Card>
                <CardHeader>
                  <CardTitle className="text-base font-mono">{result.query}</CardTitle>
                  <CardDescription>
                    {result.steps.length} steps, {result.total_latency_ms.toFixed(2)}ms total
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <GraphDiagram steps={result.steps} />

                  {result.final_answer && (
                    <div className="rounded-md border border-good/30 bg-good/10 p-3 text-sm">
                      <span className="font-semibold text-good">Answer: </span>
                      {result.final_answer}
                    </div>
                  )}
                  {result.escalation_reason && (
                    <div className="rounded-md border border-critical/30 bg-critical/10 p-3 text-sm">
                      <span className="font-semibold text-critical">Escalated to human: </span>
                      {result.escalation_reason}
                    </div>
                  )}

                  <div>
                    <p className="mb-2 text-xs font-medium text-muted-foreground">Execution trace</p>
                    <StepTrace steps={result.steps} />
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="flex h-full min-h-48 items-center justify-center text-sm text-muted-foreground">
                Run a query to see the graph traversal here.
              </Card>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
