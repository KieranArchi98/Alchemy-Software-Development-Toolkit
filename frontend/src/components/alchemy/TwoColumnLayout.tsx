import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface TwoColumnLayoutProps {
  left: ReactNode;
  right: ReactNode;
  className?: string;
}

export function TwoColumnLayout({ left, right, className }: TwoColumnLayoutProps) {
  return (
    <div className={cn("flex h-screen w-full bg-background", className)}>
      {/* Left Column - Specification */}
      <div className="flex-1 flex flex-col border-r border-border overflow-hidden">
        {left}
      </div>

      {/* Right Column - AI Interaction */}
      <div className="w-[420px] flex-shrink-0 flex flex-col overflow-hidden border-l border-border">
        {right}
      </div>
    </div>
  );
}
