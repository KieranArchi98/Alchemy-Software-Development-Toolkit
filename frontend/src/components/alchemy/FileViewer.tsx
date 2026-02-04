import { cn } from "@/lib/utils";
import { X, FileText } from "lucide-react";
import { ProjectFile } from "./FileCarousel";

interface FileViewerProps {
  file: ProjectFile;
  onClose: () => void;
  className?: string;
}

export function FileViewer({ file, onClose, className }: FileViewerProps) {
  return (
    <div className={cn("h-full flex flex-col", className)}>
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-border mb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-surface-sunken">
            <FileText className="w-4 h-4 text-text-secondary" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-foreground">{file.name}</h3>
            <p className="text-xs text-text-tertiary">Read-only</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-2 rounded-full hover:bg-accent text-text-secondary hover:text-foreground"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto">
        <pre className="text-sm text-text-secondary font-mono leading-relaxed whitespace-pre-wrap p-4 rounded-xl bg-surface-sunken">
          {file.content}
        </pre>
      </div>
    </div>
  );
}
