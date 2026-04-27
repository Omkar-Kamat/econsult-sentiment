export default function TypingIndicator() {
  return (
    <div className="flex gap-3 items-center">
      <div className="w-8 h-8 rounded-full bg-bg-raised border border-border
                      flex items-center justify-center shrink-0">
        <span className="text-text-muted text-xs">AI</span>
      </div>
      <div className="bg-bg-raised border border-border rounded-xl px-4 py-3 flex gap-1.5">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="w-1.5 h-1.5 rounded-full bg-text-muted animate-typing"
            style={{ animationDelay: `${i * 0.2}s` }}
          />
        ))}
      </div>
    </div>
  )
}