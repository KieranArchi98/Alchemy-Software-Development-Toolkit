import { useState } from "react";
import { ArrowLeft, Download, Settings as SettingsIcon } from "lucide-react";
import { TwoColumnLayout } from "./TwoColumnLayout";
import { ProgressIndicator } from "./ProgressIndicator";
import { CheckpointIndicator } from "./CheckpointIndicator";
import { SpecificationView } from "./SpecificationView";
import { FileCarousel, ProjectFile } from "./FileCarousel";
import { FileViewer } from "./FileViewer";
import { ChatPanel } from "./ChatPanel";
import { Project } from "@/types/project";
import { AIMode } from "./ModeSelector";

interface WorkspaceProps {
  project: Project;
  isLoading?: boolean;
  onSendMessage: (content: string, mode: AIMode) => void;
  onSelectOption: (messageId: string, optionId: string) => void;
  onUseDefault: (messageId: string) => void;
  onRevert: () => void;
  onBack?: () => void;
}

export function Workspace({
  project,
  isLoading,
  onSendMessage,
  onSelectOption,
  onUseDefault,
  onRevert,
  onBack,
}: WorkspaceProps) {
  const [activeFile, setActiveFile] = useState<ProjectFile | null>(null);

  const handleFileSelect = (file: ProjectFile) => {
    if (file.id === 'spec-default') {
      setActiveFile(null);
    } else {
      setActiveFile(file);
    }
  };

  const handleCloseFile = () => {
    setActiveFile(null);
  };

  const leftColumn = (
    <div className="flex flex-col h-full bg-background">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0 mr-4">
            <h2 className="text-lg font-semibold text-foreground mb-1 truncate">
              {project.title}
            </h2>
            <p className="text-sm text-text-tertiary line-clamp-1">
              {project.idea}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <ProgressIndicator
              progress={project.progress}
              showLabel
              className="flex-shrink-0"
            />
          </div>
        </div>
        <CheckpointIndicator
          lastSaved={project.lastSaved}
        />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 overflow-y-auto p-6">
        {activeFile ? (
          <FileViewer file={activeFile} onClose={handleCloseFile} />
        ) : (
          <SpecificationView sections={project.sections} />
        )}
      </div>

      {/* File Carousel */}
      <div className="p-4 border-t border-border bg-surface-sunken">
        <p className="text-xs text-text-tertiary uppercase tracking-wider mb-3 font-medium">
          Project Files
        </p>
        <FileCarousel
          files={project.files}
          activeFileId={activeFile?.id ?? null}
          onFileSelect={handleFileSelect}
        />
      </div>
    </div>
  );

  const rightColumn = (
    <ChatPanel
      messages={project.messages}
      isLoading={isLoading}
      onSendMessage={onSendMessage}
      onSelectOption={onSelectOption}
      onUseDefault={onUseDefault}
      onBack={onBack}
    />
  );

  return <TwoColumnLayout left={leftColumn} right={rightColumn} />;
}
