import { cn } from "@/lib/utils";
import { useState, useRef, useEffect } from "react";
import { ArrowUp, Paperclip, ArrowLeft, Download, Settings as SettingsIcon } from "lucide-react";
import { ModeSelector, AIMode, getPlaceholderForMode } from "./ModeSelector";
import { MessageCard, Message } from "./MessageCard";

interface ChatPanelProps {
  messages: Message[];
  isLoading?: boolean;
  onSendMessage: (content: string, mode: AIMode) => void;
  onSelectOption: (messageId: string, optionId: string) => void;
  onUseDefault: (messageId: string) => void;
  onBack?: () => void;
  className?: string;
}

export function ChatPanel({
  messages,
  isLoading,
  onSendMessage,
  onSelectOption,
  onUseDefault,
  onBack,
  className,
}: ChatPanelProps) {
  const [mode, setMode] = useState<AIMode>("guided");
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    onSendMessage(input.trim(), mode);
    setInput("");
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className={cn("flex flex-col h-full bg-background", className)}>
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold text-foreground">AI Assistant</h3>
            {mode === "research" && (
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-accent text-text-secondary font-bold uppercase tracking-wider">
                Research
              </span>
            )}
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={onBack}
              title="Back"
              className="p-1.5 rounded-md hover:bg-accent text-text-tertiary hover:text-foreground transition-all duration-200"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <button title="Export" className="p-1.5 rounded-md hover:bg-accent text-text-tertiary hover:text-foreground transition-all duration-200">
              <Download className="w-4 h-4" />
            </button>
            <button title="Settings" className="p-1.5 rounded-md hover:bg-accent text-text-tertiary hover:text-foreground transition-all duration-200">
              <SettingsIcon className="w-4 h-4" />
            </button>
          </div>
        </div>
        <ModeSelector activeMode={mode} onModeChange={setMode} />
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-sm text-text-tertiary text-center">
              Start a conversation to build your specification.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <MessageCard
              key={message.id}
              message={message}
              onSelectOption={onSelectOption}
              onUseDefault={onUseDefault}
            />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-border">
        <div className="relative rounded-full shadow-soft hover:shadow-medium transition-shadow">
          <div className="flex items-center">
            <button
              type="button"
              className="absolute left-3 p-2 rounded-full text-text-tertiary hover:text-text-secondary hover:bg-accent"
            >
              <Paperclip className="w-4 h-4" />
            </button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              placeholder={isLoading ? "AI is thinking..." : getPlaceholderForMode(mode)}
              className={cn(
                "w-full pl-12 pr-14 py-3.5 rounded-full",
                "text-sm text-foreground placeholder:text-text-tertiary",
                "bg-surface-sunken border border-border",
                "focus:outline-none focus:ring-2 focus:ring-ring/10",
                isLoading && "opacity-50 cursor-not-allowed"
              )}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className={cn(
                "absolute right-2 btn-icon btn-icon-sm",
                (!input.trim() || isLoading) && "bg-muted text-muted-foreground"
              )}
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-t-transparent border-foreground rounded-full animate-spin" />
              ) : (
                <ArrowUp className="w-4 h-4" />
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
