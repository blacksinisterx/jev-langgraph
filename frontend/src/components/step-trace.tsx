import { AlertTriangle } from "lucide-react";
import { NodeBadge } from "./node-badge";
import type { TraceStep } from "@/types";

export function StepTrace({ steps }: { steps: TraceStep[] }) {
  return (
    <ol className="space-y-2">
      {steps.map((step, i) => (
        <li key={i} className="flex items-start gap-3 rounded-md border p-2.5 text-sm">
          <span className="mt-0.5 w-5 shrink-0 text-right font-mono text-xs text-muted-foreground">{i + 1}</span>
          <NodeBadge node={step.node} className="shrink-0" />
          <div className="min-w-0 flex-1 space-y-1">
            <p className={step.failed ? "text-critical" : ""}>
              {step.failed && <AlertTriangle className="mr-1 inline size-3.5" />}
              {step.detail}
            </p>
            {step.decision && (
              <p className="font-mono text-xs text-muted-foreground">
                Jev: {step.decision.choice} ({(step.decision.confidence * 100).toFixed(0)}% confidence, {step.decision.latency_ms.toFixed(3)}ms)
              </p>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}
