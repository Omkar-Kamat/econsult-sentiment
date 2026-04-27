import { useClusters } from '../hooks/useClusters'
import NotebookFigure from '../components/ui/NotebookFigure'
import ClusterCard from '../components/clusters/ClusterCard'
import { Skeleton } from '../components/ui/LoadingSkeleton'

export default function ClusterExplorer() {
  const { data: clusters, isLoading } = useClusters()

  return (
    <div className="space-y-10 animate-slide-up">

      {/* UMAP — hero figure, full width */}
      <section>
        <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-4">
          Complaint Landscape (UMAP)
        </h2>
        <NotebookFigure
          figureKey="04_umap_visualization"
          title="2-D Complaint Embedding Landscape"
          subtitle="20,000 complaints projected to 2 dimensions. Each point is a complaint. Colour = cluster."
          notebook="NB04 — Topic Clustering"
          note="UMAP preserves local semantic structure. Visually distinct colour regions confirm that the three clusters have genuine separable structure in the original 384-dimensional embedding space."
        />
      </section>

      {/* K-selection + ROUGE side by side */}
      <section>
        <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-4">
          Model Validation
        </h2>
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <NotebookFigure
            figureKey="04_k_selection"
            title="Optimal Cluster Count Selection"
            subtitle="Silhouette score and inertia elbow plot for k=3 to 10."
            notebook="NB04 — Topic Clustering"
            note="The silhouette score peaks at k=3, confirming three as the natural number of complaint themes."
          />
          <NotebookFigure
            figureKey="06_rouge_scores"
            title="T5 Summary Consistency"
            subtitle="Pairwise ROUGE-1/2/L scores between 5 independent summaries per cluster."
            notebook="NB06 — Summarisation"
            note="High pairwise ROUGE scores confirm each cluster produces consistent summaries regardless of which complaints are sampled — validating cluster coherence."
          />
        </div>
      </section>

      {/* Word clouds */}
      <section>
        <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-4">
          Cluster Vocabulary
        </h2>
        <NotebookFigure
          figureKey="06_wordclouds"
          title="Cluster Word Clouds"
          subtitle="Dominant vocabulary for Credit Report Disputes, Debt Collection, and Card Payments."
          notebook="NB06 — Summarisation"
          note="Word size = TF-IDF-weighted term frequency within the cluster. Confirms distinct lexical profiles: bureau/dispute · debt/collector · payment/charge."
        />
      </section>

      {/* Cluster cards */}
      <section>
        <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-4">
          Cluster Details
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {isLoading
            ? Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="rounded-xl border border-border bg-bg-surface p-5 space-y-3">
                  <Skeleton className="h-5 w-32" />
                  <Skeleton className="h-3 w-full" />
                  <Skeleton className="h-3 w-3/4" />
                </div>
              ))
            : clusters?.clusters.map((c) => <ClusterCard key={c.id} cluster={c} />)
          }
        </div>
      </section>
    </div>
  )
}