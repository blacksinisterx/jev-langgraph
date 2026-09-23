import type { TraceStep } from "@/types";

const POS: Record<string, { x: number; y: number; w: number; h: number }> = {
  decide: { x: 310, y: 55, w: 100, h: 40 },
  search: { x: 90, y: 175, w: 100, h: 40 },
  use_tool: { x: 310, y: 175, w: 100, h: 40 },
  retry: { x: 530, y: 175, w: 100, h: 40 },
  finish: { x: 210, y: 295, w: 100, h: 40 },
  escalate: { x: 430, y: 295, w: 100, h: 40 },
};

const NODE_COLOR: Record<string, string> = {
  decide: "#3987e5",
  search: "#8a8a86",
  use_tool: "#8a8a86",
  retry: "#eb6834",
  finish: "#0ca30c",
  escalate: "#d03b3b",
};

const SATELLITES = ["search", "use_tool", "retry"] as const;

function center(id: string) {
  const p = POS[id];
  return { x: p.x + p.w / 2, y: p.y + p.h / 2 };
}

export function GraphDiagram({ steps }: { steps: TraceStep[] }) {
  const visitedNodes = new Set(steps.map((s) => s.node));
  const usedContinueLoop = steps.some((s) => s.node === "decide" && s.decision?.choice === "continue");
  const decideC = center("decide");

  return (
    <svg viewBox="0 0 700 365" className="w-full" role="img" aria-label="JevGraph state diagram, with nodes visited in this run highlighted">
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" fill="currentColor" />
        </marker>
      </defs>

      {/* decide <-> satellites, bidirectional */}
      {SATELLITES.map((id) => {
        const c = center(id);
        const active = visitedNodes.has(id);
        return (
          <line
            key={id}
            x1={decideC.x} y1={decideC.y} x2={c.x} y2={c.y}
            stroke={active ? NODE_COLOR[id] : "currentColor"}
            strokeOpacity={active ? 0.8 : 0.2}
            strokeWidth={active ? 2 : 1.5}
            markerEnd="url(#arrow)"
            markerStart="url(#arrow)"
          />
        );
      })}

      {/* decide -> finish / escalate, one-directional */}
      {(["finish", "escalate"] as const).map((id) => {
        const c = center(id);
        const active = visitedNodes.has(id);
        return (
          <line
            key={id}
            x1={decideC.x} y1={decideC.y + 20} x2={c.x} y2={c.y - 15}
            stroke={active ? NODE_COLOR[id] : "currentColor"}
            strokeOpacity={active ? 0.8 : 0.2}
            strokeWidth={active ? 2 : 1.5}
            markerEnd="url(#arrow)"
          />
        );
      })}

      {/* decide self-loop for "continue" */}
      <path
        d={`M ${decideC.x - 20} ${POS.decide.y - 3} C ${decideC.x - 50} ${POS.decide.y - 45}, ${decideC.x + 50} ${POS.decide.y - 45}, ${decideC.x + 20} ${POS.decide.y - 3}`}
        fill="none"
        stroke={usedContinueLoop ? NODE_COLOR.decide : "currentColor"}
        strokeOpacity={usedContinueLoop ? 0.8 : 0.2}
        strokeWidth={usedContinueLoop ? 2 : 1.5}
        markerEnd="url(#arrow)"
      />
      <text x={decideC.x} y={POS.decide.y - 38} textAnchor="middle" fontSize={9} fill="currentColor" opacity={0.6}>continue</text>

      {Object.entries(POS).map(([id, p]) => {
        const active = visitedNodes.has(id);
        const visitCount = steps.filter((s) => s.node === id).length;
        return (
          <g key={id}>
            <rect
              x={p.x} y={p.y} width={p.w} height={p.h} rx={8}
              fill={active ? `${NODE_COLOR[id]}22` : "transparent"}
              stroke={active ? NODE_COLOR[id] : "currentColor"}
              strokeOpacity={active ? 1 : 0.35}
              strokeWidth={active ? 2 : 1.5}
            />
            <text x={p.x + p.w / 2} y={p.y + p.h / 2 + 4} textAnchor="middle" fontSize={12} fontFamily="ui-monospace, monospace"
              fill={active ? NODE_COLOR[id] : "currentColor"} opacity={active ? 1 : 0.5} fontWeight={active ? 600 : 400}>
              {id}
            </text>
            {active && visitCount > 1 && (
              <text
                x={p.x + p.w - 4}
                y={id === "decide" ? p.y + p.h + 12 : p.y - 4}
                textAnchor="end" fontSize={9} fill="currentColor" opacity={0.6}
              >
                x{visitCount}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}
