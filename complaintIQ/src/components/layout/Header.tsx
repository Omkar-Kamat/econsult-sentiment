import { useLocation } from 'react-router-dom'

const PAGE_META: Record<string, { title: string; description: string }> = {
  '/':         { title: 'Dashboard',        description: 'Overview of complaint analytics and model performance' },
  '/bot':      { title: 'Complaint Bot',    description: 'AI-powered complaint classification and response generation' },
  '/clusters': { title: 'Cluster Explorer', description: 'Deep-dive into the three AI-discovered complaint clusters' },
  '/insights': { title: 'Research Insights', description: 'All notebook figures and ML methodology documentation' },
  '/history':  { title: 'History',           description: 'Complaint processing and response history' },
}

export default function Header() {
  const { pathname } = useLocation()
  const meta = PAGE_META[pathname] ?? PAGE_META['/']

  return (
    <header className="h-16 border-b border-border bg-bg-surface px-8 flex items-center justify-between shrink-0">
      <div>
        <h1 className="font-body text-base font-semibold text-text-primary">
          {meta.title}
        </h1>
        <p className="font-body text-xs text-text-muted mt-0.5">
          {meta.description}
        </p>
      </div>

      {/* Live indicator */}
      <div className="flex items-center gap-2 font-display text-[11px] text-text-muted tracking-widest uppercase">
        <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse-slow" />
        Live
      </div>
    </header>
  )
}