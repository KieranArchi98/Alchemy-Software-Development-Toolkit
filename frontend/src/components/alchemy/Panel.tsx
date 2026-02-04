import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface PanelProps {
  children: ReactNode;
  className?: string;
  elevated?: boolean;
}

export function Panel({ children, className, elevated = false }: PanelProps) {
  return (
    <div
      className={cn(
        "rounded-lg border border-border",
        elevated ? "bg-surface-elevated shadow-sm" : "bg-card",
        className
      )}
    >
      {children}
    </div>
  );
}

interface PanelHeaderProps {
  children: ReactNode;
  className?: string;
}

export function PanelHeader({ children, className }: PanelHeaderProps) {
  return (
    <div className={cn("px-5 py-4 border-b border-border", className)}>
      {children}
    </div>
  );
}

interface PanelContentProps {
  children: ReactNode;
  className?: string;
}

export function PanelContent({ children, className }: PanelContentProps) {
  return <div className={cn("p-5", className)}>{children}</div>;
}
