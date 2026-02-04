import { cn } from "@/lib/utils";
import { RotateCcw, Check } from "lucide-react";
import { useState } from "react";

interface CheckpointIndicatorProps {
  lastSaved: string | null;
  className?: string;
}

export function CheckpointIndicator({
  lastSaved,
  className,
}: CheckpointIndicatorProps) {

  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="flex items-center gap-2 text-xs text-text-tertiary">
        <Check className="w-3.5 h-3.5" />
        <span>
          {lastSaved
            ? `Saved at ${formatTime(lastSaved)}`
            : "Not saved yet"}
        </span>
      </div>
    </div>
  );
}
