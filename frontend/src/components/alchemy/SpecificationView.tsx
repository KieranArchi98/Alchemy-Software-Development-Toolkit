import { cn } from "@/lib/utils";

export interface SpecSection {
  id: string;
  title: string;
  content: string;
  subsections?: { title: string; content: string }[];
}

interface SpecificationViewProps {
  sections: SpecSection[];
  className?: string;
}

export function SpecificationView({ sections, className }: SpecificationViewProps) {
  return (
    <div className={cn("space-y-8", className)}>
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-foreground mb-1">
          Living Specification
        </h2>
        <p className="text-sm text-text-tertiary">
          Your project specification evolves as you refine your idea
        </p>
      </div>

      {sections.map((section) => (
        <section key={section.id} className="space-y-4">
          <h3 className="text-base font-semibold text-foreground pb-2 border-b border-border">
            {section.title}
          </h3>
          
          <div className="text-sm text-text-secondary leading-relaxed whitespace-pre-wrap">
            {section.content || (
              <span className="italic text-text-tertiary">Not yet defined...</span>
            )}
          </div>

          {section.subsections && section.subsections.length > 0 && (
            <div className="space-y-4 pl-4 border-l-2 border-border">
              {section.subsections.map((sub, idx) => (
                <div key={idx}>
                  <h4 className="text-sm font-medium text-foreground mb-2">
                    {sub.title}
                  </h4>
                  <p className="text-sm text-text-secondary leading-relaxed">
                    {sub.content}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>
      ))}
    </div>
  );
}
