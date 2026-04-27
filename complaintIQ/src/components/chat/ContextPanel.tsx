import type { ClassifyResponse, RespondResponse } from '../../types'
import NotebookFigure from '../ui/NotebookFigure'
import ClusterBadge from '../ui/ClusterBadge'
import { useClusters } from '../../hooks/useClusters'

interface ContextPanelProps {
  classification: ClassifyResponse | null
  response: RespondResponse | null
}

export default function ContextPanel({ classification, response }: ContextPanelProps) {
  const { data: clusters } = useClusters()
  const activeCluster = clusters?.clusters.find(
    (c) => c.id === classification?.cluster_id
  )

  return (
    <div className="flex flex-col h-full gap-4 overflow-y-auto">

      {/* VADER figure — always shown */}
      <NotebookFigure
        figureKey="03_vader_sentiment"
        title="Sentiment Distribution"
        subtitle="Where complaints fall on the VADER sentiment scale."
        notebook="NB03 — Preprocessing"
      />

      {/* Cluster context — shown after classification */}
      {classification && activeCluster && (
        <div className="rounded-xl border border-border bg-bg-surface p-4 space-y-3 animate-slide-up">
          <div className="flex items-center justify-between">
            <p className="font-display text-[10px] text-text-muted tracking-widest uppercase">
              Matched Cluster
            </p>
            <ClusterBadge
              clusterId={classification.cluster_id}
              label={classification.cluster_label}
              size="sm"
            />
          </div>
          <p className="font-body text-xs text-text-secondary leading-relaxed">
            {activeCluster.context}
          </p>
          <div className="flex flex-wrap gap-1.5">
            {activeCluster.top_keywords.map((kw) => (
              <span key={kw} className="font-display text-[10px] text-text-muted
                                        bg-bg-raised border border-border px-2 py-0.5 rounded">
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Response confidence — shown after response */}
      {response && (
        <div className="rounded-xl border border-border bg-bg-surface p-4 animate-slide-up">
          <p className="font-display text-[10px] text-text-muted tracking-widest uppercase mb-3">
            Response Confidence
          </p>
          <div className="h-2 bg-bg-raised rounded-full overflow-hidden">
            <div
              className="h-full bg-accent rounded-full transition-all duration-700"
              style={{ width: `${response.confidence * 100}%` }}
            />
          </div>
          <p className="font-display text-xs text-text-secondary mt-1.5">
            {(response.confidence * 100).toFixed(0)}% · {response.processing_ms}ms
          </p>
        </div>
      )}
    </div>
  )
}