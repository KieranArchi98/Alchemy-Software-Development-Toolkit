import { useState } from "react";
import { ArrowUp, Paperclip, Zap, Compass, Search, FileEdit, Trash2, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

interface LandingProps {
  onCreateProject: (idea: string) => void;
  onLoadProject: (projectId: string) => void;
  onDeleteProject: (projectId: string) => void;
  isLoading?: boolean;
  recentProjects?: any[];
}

const quickActions = [
  { id: "guided", label: "Guided", icon: Compass },
  { id: "research", label: "Research", icon: Search },
  { id: "update", label: "Update", icon: FileEdit },
];

export function Landing({ onCreateProject, onLoadProject, onDeleteProject, isLoading, recentProjects = [] }: LandingProps) {
  const [idea, setIdea] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (idea.trim()) {
      onCreateProject(idea.trim());
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const hasProjects = recentProjects.length > 0;

  return (
    <div className="min-h-screen w-full flex flex-col items-center px-6 bg-background overflow-y-auto pt-24 pb-20">
      <div className={cn(
        "w-full max-w-2xl animate-fade-in flex flex-col justify-center",
        hasProjects ? "min-h-[50vh]" : "min-h-[75vh]"
      )}>
        {/* Logo/Title */}
        <div className="text-center mb-12">
          <h1 className="font-display text-5xl font-bold text-foreground tracking-tight mb-3 flex items-center justify-center gap-3">
            <svg
              className="w-12 h-12"
              viewBox="0 0 48 48"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M24 4L28 16L40 20L28 24L24 36L20 24L8 20L20 16L24 4Z"
                fill="currentColor"
                className="text-foreground"
              />
              <path
                d="M36 28L38 34L44 36L38 38L36 44L34 38L28 36L34 34L36 28Z"
                fill="currentColor"
                className="text-foreground opacity-60"
              />
            </svg>
            Alchemy
          </h1>
          <p className="text-lg text-text-secondary">
            What do you want to build?
          </p>
        </div>

        {/* Main Input Area */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div
            className={cn(
              "relative rounded-full transition-all duration-300",
              "shadow-soft hover:shadow-medium",
              isFocused && "shadow-medium ring-2 ring-ring/10"
            )}
          >
            <div className="flex items-center">
              {/* Attachment Button */}
              <button
                type="button"
                className="absolute left-4 p-2 rounded-full text-text-tertiary hover:text-text-secondary hover:bg-accent"
              >
                <Paperclip className="w-5 h-5" />
              </button>

              {/* Input */}
              <input
                type="text"
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                onFocus={() => setIsFocused(true)}
                onBlur={() => setIsFocused(false)}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
                placeholder={isLoading ? "Analyzing your idea..." : "Describe your project idea..."}
                className={cn(
                  "w-full pl-14 pr-32 py-5 bg-surface-sunken rounded-full",
                  "text-base text-foreground placeholder:text-text-tertiary",
                  "focus:outline-none",
                  "border border-border",
                  isLoading && "opacity-50 cursor-not-allowed"
                )}
              />

              {/* Right side controls */}
              <div className="absolute right-3 flex items-center gap-2">
                {/* Mode indicator */}
                <button
                  type="button"
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium text-text-secondary hover:bg-accent"
                >
                  <Zap className="w-4 h-4" />
                  <span>Fast</span>
                </button>

                {/* Submit button */}
                <button
                  type="submit"
                  disabled={!idea.trim() || isLoading}
                  className={cn(
                    "btn-icon btn-icon-sm",
                    (!idea.trim() || isLoading) && "bg-muted text-muted-foreground"
                  )}
                >
                  {isLoading ? (
                    <div className="w-5 h-5 border-2 border-t-transparent border-foreground rounded-full animate-spin" />
                  ) : (
                    <ArrowUp className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center justify-center gap-3 pt-2">
            {quickActions.map((action) => {
              const Icon = action.icon;
              return (
                <button
                  key={action.id}
                  type="button"
                  className="quick-action"
                  onClick={() => {
                    // Could set different modes or pre-fill templates
                  }}
                >
                  <Icon className="w-4 h-4" />
                  <span>{action.label}</span>
                </button>
              );
            })}
          </div>
        </form>
      </div>

      {recentProjects.length > 0 && (
        <div className="w-full max-w-5xl mt-10 animate-fade-in-up">
          <div className="flex items-center justify-between mb-8 px-2">
            <h2 className="text-sm font-bold text-text-tertiary uppercase tracking-[0.2em]">
              Recent Architectures
            </h2>
            <div className="h-px flex-grow bg-gradient-to-r from-border/50 to-transparent ml-6" />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {recentProjects.map((project) => (
              <div
                key={project.id}
                onClick={() => onLoadProject(project.id)}
                className={cn(
                  "group relative overflow-hidden",
                  "bg-surface border border-border rounded-2xl p-6",
                  "hover:border-ring/40 hover:shadow-medium hover:-translate-y-1",
                  "transition-all duration-300 cursor-pointer"
                )}
              >
                {/* Progress Glow */}
                <div
                  className="absolute bottom-0 left-0 h-1 bg-ring transition-all duration-500 opacity-30"
                  style={{ width: `${project.progress}%` }}
                />

                <div className="flex flex-col h-full gap-4">
                  <div className="flex items-start justify-between gap-2">
                    <div className="p-2 rounded-xl bg-accent text-accent-foreground">
                      <Zap className="w-4 h-4" />
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteProject(project.id);
                      }}
                      className="p-2 text-text-tertiary hover:text-destructive hover:bg-destructive/10 rounded-full transition-colors opacity-0 group-hover:opacity-100"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <div>
                    <h3 className="font-semibold text-foreground text-lg mb-1 leading-tight line-clamp-1">
                      {project.title}
                    </h3>
                    <p className="text-sm text-text-secondary line-clamp-2 h-10">
                      {project.idea}
                    </p>
                  </div>

                  <div className="flex items-center justify-between mt-auto">
                    <div className="flex items-center gap-2 text-xs text-text-tertiary">
                      <Clock className="w-3 h-3" />
                      <span>{new Date(project.lastSaved).toLocaleDateString('en-GB')}</span>
                    </div>
                    <div className="px-2.5 py-1 rounded-full bg-ring/10 text-ring text-[10px] font-bold uppercase tracking-wider">
                      {project.progress}% Done
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Subtle footer hint */}
      <p className="text-center text-sm text-text-tertiary mt-32">
        Transform your idea into an AI-ready specification
      </p>
    </div>
  );
}
