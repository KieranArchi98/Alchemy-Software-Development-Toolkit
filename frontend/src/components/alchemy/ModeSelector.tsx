import { cn } from "@/lib/utils";
import { Compass, Search, FileEdit } from "lucide-react";

export type AIMode = "guided" | "research" | "update";

interface ModeSelectorProps {
  activeMode: AIMode;
  onModeChange: (mode: AIMode) => void;
  className?: string;
}

const modes: { id: AIMode; label: string; icon: typeof Compass }[] = [
  {
    id: "guided",
    label: "Guided",
    icon: Compass,
  },
  {
    id: "research",
    label: "Research",
    icon: Search,
  },
  {
    id: "update",
    label: "Update",
    icon: FileEdit,
  },
];

export function ModeSelector({ activeMode, onModeChange, className }: ModeSelectorProps) {
  return (
    <div className={cn("flex items-center gap-1", className)}>
      {modes.map((mode) => {
        const Icon = mode.icon;
        const isActive = activeMode === mode.id;

        return (
          <button
            key={mode.id}
            onClick={() => onModeChange(mode.id)}
            className={cn(
              "mode-pill flex items-center gap-2",
              isActive && "mode-pill-active"
            )}
          >
            <Icon className="w-4 h-4" />
            <span>{mode.label}</span>
          </button>
        );
      })}
    </div>
  );
}

export function getPlaceholderForMode(mode: AIMode): string {
  switch (mode) {
    case "guided":
      return "Continue building your specification...";
    case "research":
      return "Ask a question (won't modify your spec)...";
    case "update":
      return "Describe what to change...";
  }
}
