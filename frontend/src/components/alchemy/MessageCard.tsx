import { cn } from "@/lib/utils";
import { useState } from "react";
import { Sparkles, Check } from "lucide-react";

export interface MessageOption {
  id: string;
  label: string;
  description?: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  context?: string; // "Why this matters" explanation
  options?: MessageOption[];
  selectedOption?: string;
  timestamp: Date;
}

interface MessageCardProps {
  message: Message;
  onSelectOption?: (messageId: string, optionId: string) => void;
  onUseDefault?: (messageId: string) => void;
  className?: string;
}

export function MessageCard({
  message,
  onSelectOption,
  onUseDefault,
  className,
}: MessageCardProps) {
  const [selectedOption, setSelectedOption] = useState<string | undefined>(
    message.selectedOption
  );

  const isUser = message.role === "user";

  const handleSelectOption = (optionId: string) => {
    setSelectedOption(optionId);
    onSelectOption?.(message.id, optionId);
  };

  return (
    <div
      className={cn(
        "animate-slide-up",
        isUser ? "flex justify-end" : "",
        className
      )}
    >
      <div
        className={cn(
          "max-w-[90%]",
          isUser
            ? "bg-zinc-900 dark:bg-zinc-800 text-white rounded-3xl rounded-br-lg px-5 py-3.5 shadow-sm border border-white/5"
            : "space-y-3"
        )}
      >
        {isUser ? (
          <p className="text-sm leading-relaxed !text-white font-medium">{message.content}</p>
        ) : (
          <>
            {/* AI Message Content */}
            <div className="message-card">
              <p className="text-sm leading-relaxed text-foreground">
                {message.content}
              </p>

              {message.context && (
                <p className="mt-3 text-xs text-text-tertiary leading-relaxed">
                  {message.context}
                </p>
              )}
            </div>

            {/* Options */}
            {message.options && message.options.length > 0 && (
              <div className="space-y-2">
                {message.options.map((option) => {
                  const isSelected = selectedOption === option.id;
                  return (
                    <button
                      key={option.id}
                      onClick={() => handleSelectOption(option.id)}
                      className={cn(
                        "option-card w-full text-left flex items-start gap-3",
                        isSelected && "option-card-selected"
                      )}
                    >
                      <div className={cn(
                        "flex-shrink-0 w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5",
                        isSelected
                          ? "border-primary bg-primary"
                          : "border-border"
                      )}>
                        {isSelected && <Check className="w-3 h-3 text-primary-foreground" />}
                      </div>
                      <div className="flex-1">
                        <p className="text-sm font-medium text-foreground">
                          {option.label}
                        </p>
                        {option.description && (
                          <p className="text-xs text-text-tertiary mt-1">
                            {option.description}
                          </p>
                        )}
                      </div>
                    </button>
                  );
                })}

                {/* Use AI Default */}
                <button
                  onClick={() => onUseDefault?.(message.id)}
                  className="flex items-center gap-2 text-xs text-text-secondary hover:text-foreground mt-2 px-1"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Use AI recommendation</span>
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
