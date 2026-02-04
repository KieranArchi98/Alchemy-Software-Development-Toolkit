import { cn } from "@/lib/utils";

interface ProgressIndicatorProps {
  progress: number; // 0-100
  showLabel?: boolean;
  className?: string;
}

export function ProgressIndicator({
  progress,
  showLabel = false,
  className,
}: ProgressIndicatorProps) {
  const clampedProgress = Math.min(100, Math.max(0, progress));

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="progress-track w-24">
        <div
          className="progress-fill"
          style={{ width: `${clampedProgress}%` }}
        />
      </div>
      {showLabel && (
        <span className="text-xs font-medium text-text-secondary tabular-nums">
          {Math.round(clampedProgress)}%
        </span>
      )}
    </div>
  );
}
