import { useState } from 'react'
import { useHistory } from '../hooks/useHistory'
import ClusterBadge from '../components/ui/ClusterBadge'
import SentimentBadge from '../components/ui/SentimentBadge'
import { Skeleton } from '../components/ui/LoadingSkeleton'
import { formatDistanceToNow } from 'date-fns'
import { ChevronLeft, ChevronRight } from 'lucide-react'

const LIMIT = 15

export default function History() {
  const [page, setPage] = useState(0)
  const [clusterFilter, setClusterFilter] = useState<number | undefined>()
  const [sentimentFilter, setSentimentFilter] = useState<string | undefined>()

  const { data, isLoading } = useHistory({
    limit: LIMIT,
    skip: page * LIMIT,
    cluster_id: clusterFilter,
    sentiment: sentimentFilter,
  })

  const totalPages = data ? Math.ceil(data.total / LIMIT) : 0

  return (
    <div className="space-y-6 animate-slide-up">

      {/* Filters */}
      <div className="flex items-center gap-3 flex-wrap">
        <p className="font-display text-[11px] text-text-muted tracking-widest uppercase">
          Filters:
        </p>

        {/* Cluster filter */}
        {[undefined, 0, 1, 2].map((id) => (
          <button
            key={String(id)}
            onClick={() => { setClusterFilter(id as number | undefined); setPage(0) }}
            className={`font-display text-xs px-3 py-1.5 rounded-full border transition-all
                        ${clusterFilter === id
                          ? 'bg-accent/10 border-accent/30 text-accent'
                          : 'border-border text-text-secondary hover:border-border-active'}`}
          >
            {id === undefined ? 'All Clusters' : `Cluster ${id}`}
          </button>
        ))}

        <div className="w-px h-5 bg-border mx-1" />

        {/* Sentiment filter */}
        {[undefined, 'negative', 'neutral', 'positive'].map((s) => (
          <button
            key={String(s)}
            onClick={() => { setSentimentFilter(s as string | undefined); setPage(0) }}
            className={`font-display text-xs px-3 py-1.5 rounded-full border transition-all
                        ${sentimentFilter === s
                          ? 'bg-accent/10 border-accent/30 text-accent'
                          : 'border-border text-text-secondary hover:border-border-active'}`}
          >
            {s ?? 'All Sentiment'}
          </button>
        ))}
      </div>

      {/* Table */}
      <div className="rounded-xl border border-border bg-bg-surface overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              {['Complaint Preview', 'Cluster', 'Sentiment', 'Words', 'Time', 'ms'].map((h) => (
                <th key={h}
                  className="px-4 py-3 text-left font-display text-[10px] text-text-muted
                             tracking-widest uppercase">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {isLoading
              ? Array.from({ length: 8 }).map((_, i) => (
                  <tr key={i} className="border-b border-border">
                    {Array.from({ length: 6 }).map((_, j) => (
                      <td key={j} className="px-4 py-3">
                        <Skeleton className="h-3 w-full" />
                      </td>
                    ))}
                  </tr>
                ))
              : data?.complaints.map((c) => (
                  <tr
                    key={c._id}
                    className="border-b border-border hover:bg-bg-raised transition-colors"
                  >
                    <td className="px-4 py-3 max-w-xs">
                      <p className="font-body text-xs text-text-secondary truncate">
                        {c.raw_text}
                      </p>
                    </td>
                    <td className="px-4 py-3">
                      <ClusterBadge clusterId={c.cluster_id} label={c.cluster_label} size="sm" />
                    </td>
                    <td className="px-4 py-3">
                      <SentimentBadge sentiment={c.sentiment} />
                    </td>
                    <td className="px-4 py-3 font-display text-xs text-text-muted">
                      {c.word_count}
                    </td>
                    <td className="px-4 py-3 font-display text-xs text-text-muted whitespace-nowrap">
                      {formatDistanceToNow(new Date(c.created_at), { addSuffix: true })}
                    </td>
                    <td className="px-4 py-3 font-display text-xs text-text-muted">
                      {c.processing_ms}
                    </td>
                  </tr>
                ))
            }
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between">
        <p className="font-display text-xs text-text-muted">
          {data ? `${data.total} total complaints` : '—'}
        </p>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="w-8 h-8 rounded-lg border border-border flex items-center justify-center
                       text-text-secondary hover:border-border-active disabled:opacity-30 transition-all"
          >
            <ChevronLeft size={14} />
          </button>
          <span className="font-display text-xs text-text-muted">
            {page + 1} / {totalPages || 1}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
            className="w-8 h-8 rounded-lg border border-border flex items-center justify-center
                       text-text-secondary hover:border-border-active disabled:opacity-30 transition-all"
          >
            <ChevronRight size={14} />
          </button>
        </div>
      </div>
    </div>
  )
}