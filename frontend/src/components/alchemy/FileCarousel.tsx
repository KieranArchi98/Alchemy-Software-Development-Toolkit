import { cn } from "@/lib/utils";
import { FileText, FileJson, ListChecks, Code } from "lucide-react";

export interface ProjectFile {
  id: string;
  name: string;
  type: "design" | "context" | "roadmap" | "prompts";
  content: string;
}

interface FileCarouselProps {
  files: ProjectFile[];
  activeFileId: string | null;
  onFileSelect: (file: ProjectFile) => void;
  className?: string;
}

const fileIcons = {
  design: FileText,
  context: FileJson,
  roadmap: ListChecks,
  prompts: Code,
};

export function FileCarousel({
  files,
  activeFileId,
  onFileSelect,
  className,
}: FileCarouselProps) {
  return (
    <div className={cn("grid grid-cols-2 sm:grid-cols-5 gap-3", className)}>
      {/* Specification Default Card */}
      <button
        onClick={() => onFileSelect({ id: 'spec-default', name: 'Specification', type: 'design', content: '' })}
        className={cn(
          "flex flex-col items-center justify-center p-3 rounded-xl border transition-all duration-200",
          "hover:border-ring/50 hover:bg-accent group",
          activeFileId === 'spec-default' || activeFileId === null
            ? "bg-ring/10 border-ring text-ring shadow-sm"
            : "bg-surface border-border text-text-secondary"
        )}
      >
        <div className={cn(
          "p-2 rounded-lg mb-2 transition-colors",
          (activeFileId === 'spec-default' || activeFileId === null) ? "bg-ring/20" : "bg-muted group-hover:bg-accent-foreground/10"
        )}>
          <FileText className="w-5 h-5" />
        </div>
        <span className="text-[10px] font-bold uppercase tracking-wider text-center line-clamp-1 w-full">
          Specification
        </span>
      </button>

      {files.map((file) => {
        const Icon = fileIcons[file.type];
        const isActive = file.id === activeFileId;

        return (
          <button
            key={file.id}
            onClick={() => onFileSelect(file)}
            className={cn(
              "flex flex-col items-center justify-center p-3 rounded-xl border transition-all duration-200",
              "hover:border-ring/50 hover:bg-accent group",
              isActive
                ? "bg-ring/10 border-ring text-ring shadow-sm"
                : "bg-surface border-border text-text-secondary"
            )}
          >
            <div className={cn(
              "p-2 rounded-lg mb-2 transition-colors",
              isActive ? "bg-ring/20" : "bg-muted group-hover:bg-accent-foreground/10"
            )}>
              <Icon className="w-5 h-5" />
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-center line-clamp-1 w-full">
              {file.name}
            </span>
          </button>
        );
      })}
    </div>
  );
}
