import { cn } from "@/lib/utils";

const COLOR: Record<string, string> = {
  decide: "#3987e5", search: "#8a8a86", use_tool: "#8a8a86",
  retry: "#eb6834", finish: "#0ca30c", escalate: "#d03b3b",
};

export function NodeBadge({ node, className }: { node: string; className?: string }) {
  const color = COLOR[node] ?? "#8a8a86";
  return (
    <span
      className={cn("inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-mono font-semibold", className)}
      style={{ color, borderColor: `${color}4d`, backgroundColor: `${color}1a` }}
    >
      <span className="size-2 rounded-full" style={{ backgroundColor: color }} />
      {node}
    </span>
  );
}
