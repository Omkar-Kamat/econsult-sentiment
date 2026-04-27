import { clsx } from 'clsx'
import type { Cluster } from '../../types'
import ClusterBadge from '../ui/ClusterBadge'

const BORDER_COLORS: Record<number, string> = {
  0: 'border-blue-500/20',
  1: 'border-violet-500/20',
  2: 'border-amber-500/20',
}

export default function ClusterCard({ cluster }: { cluster: Cluster }) {
  return (
    <div className={clsx(
      'rounded-xl border bg-bg-surface p-5 space-y-4 hover:border-border-active transition-colors',
      BORDER_COLORS[cluster.id]
    )}>
      {/* Header */}
      <div className="flex items-start justify-between">
        <ClusterBadge clusterId={cluster.id} label={cluster.label} />
        <span className="font-display text-lg text-text-primary">
          {cluster.pct}%
        </span>
      </div>

      {/* Context */}
      <p className="font-body text-xs text-text-secondary leading-relaxed line-clamp-3">
        {cluster.context}
      </p>

      {/* Keywords */}
      <div className="flex flex-wrap gap-1.5">
        {cluster.top_keywords.slice(0, 5).map((kw) => (
          <span
            key={kw}
            className="font-display text-[10px] text-text-muted bg-bg-raised
                       border border-border px-2 py-0.5 rounded"
          >
            {kw}
          </span>
        ))}
      </div>

      {/* Sentiment bar */}
      <div>
        <p className="font-display text-[10px] text-text-muted mb-1.5 tracking-wide uppercase">
          Sentiment
        </p>
        <div className="flex h-1.5 rounded-full overflow-hidden gap-px">
          <div
            style={{ width: `${cluster.sentiment_breakdown.negative ?? 0}%` }}
            className="bg-sentiment-negative"
          />
          <div
            style={{ width: `${cluster.sentiment_breakdown.neutral ?? 0}%` }}
            className="bg-sentiment-neutral"
          />
          <div
            style={{ width: `${cluster.sentiment_breakdown.positive ?? 0}%` }}
            className="bg-sentiment-positive"
          />
        </div>
        <div className="flex justify-between font-display text-[10px] text-text-muted mt-1">
          <span>neg {cluster.sentiment_breakdown.negative?.toFixed(0)}%</span>
          <span>pos {cluster.sentiment_breakdown.positive?.toFixed(0)}%</span>
        </div>
      </div>
    </div>
  )
}