import {
  FileText, Brain, Layers, BarChart3
} from 'lucide-react'
import { useAnalytics } from '../hooks/useAnalytics'
import { useClusters } from '../hooks/useClusters'
import StatCard from '../components/ui/StatCard'
import NotebookFigure from '../components/ui/NotebookFigure'
import ClusterCard from '../components/clusters/ClusterCard'
import { StatCardSkeleton, FigureSkeleton, Skeleton } from '../components/ui/LoadingSkeleton'

export default function Dashboard() {
  const { data: analytics, isLoading: analyticsLoading } = useAnalytics()
  const { data: clusters, isLoading: clustersLoading } = useClusters()

  return (
    <div className="space-y-8 animate-slide-up">

      {/* ── Section: Stat Cards ─────────────────────────────────── */}
      <section>
        <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-4">
          Overview
        </h2>
        <div className="grid grid-cols-2 xl:grid-cols-4 gap-4">
          {analyticsLoading ? (
            Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
          ) : (
            <>
              <StatCard
                label="Complaints Processed"
                value={analytics?.live.total_complaints_processed.toLocaleString() ?? '—'}
                sub="Via API since launch"
                icon={FileText}
                accent
              />
              <StatCard
                label="BERT Accuracy"
                value={analytics
                  ? `${(analytics.model_metrics.bert_test_accuracy * 100).toFixed(1)}%`
                  : '—'}
                sub={`Macro F1: ${analytics
                  ? (analytics.model_metrics.bert_test_f1_macro * 100).toFixed(1)
                  : '—'}%`}
                icon={Brain}
              />
              <StatCard
                label="Active Clusters"
                value={analytics?.dataset_stats.num_clusters ?? '—'}
                sub="K-Means k=3 (silhouette-optimal)"
                icon={Layers}
              />
              <StatCard
                label="Avg. Word Count"
                value={analytics?.dataset_stats.avg_word_count ?? '—'}
                sub={`Median: ${analytics?.dataset_stats.median_word_count ?? '—'} words`}
                icon={BarChart3}
              />
            </>
          )}
        </div>
      </section>

      {/* ── Section: Notebook Figures (top 2) ───────────────────── */}
      <section>
        <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-4">
          Dataset Snapshot
        </h2>
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <NotebookFigure
            figureKey="01_class_distributions"
            title="Complaint Class Distributions"
            subtitle="Product category balance and company response types across the 20,000-row sample."
            notebook="NB02 — EDA"
            note="Credit Reporting was capped at 40% during stratified sampling to prevent model bias."
          />
          <NotebookFigure
            figureKey="02_word_count_analysis"
            title="Word Count Analysis"
            subtitle="Histogram and per-product box plots used to set BERT MAX_LEN=128."
            notebook="NB02 — EDA"
            note="95th percentile complaint is 247 words. Median is 91 words."
          />
        </div>
      </section>

      {/* ── Section: Cluster Cards ───────────────────────────────── */}
      <section>
        <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-4">
          Complaint Clusters
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {clustersLoading ? (
            Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="rounded-xl border border-border bg-bg-surface p-5 space-y-3">
                <Skeleton className="h-5 w-32" />
                <Skeleton className="h-3 w-48" />
                <Skeleton className="h-10 w-full" />
              </div>
            ))
          ) : (
            clusters?.clusters.map((cluster) => (
              <ClusterCard key={cluster.id} cluster={cluster} />
            ))
          )}
        </div>
      </section>
    </div>
  )
}