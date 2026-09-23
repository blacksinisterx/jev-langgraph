export interface Decision {
  choice: string;
  confidence: number;
  probabilities: Record<string, number>;
  latency_ms: number;
}

export interface TraceStep {
  node: string;
  detail: string;
  failed: boolean;
  decision: Decision | null;
}

export interface RunResult {
  query: string;
  steps: TraceStep[];
  final_answer: string | null;
  escalation_reason: string | null;
  provider: string;
  total_latency_ms: number;
}

export interface DemoQuery {
  category: string;
  query: string;
}

export interface GraphSchema {
  nodes: string[];
  edges: { from: string; to: string }[];
}
