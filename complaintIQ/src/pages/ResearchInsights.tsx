import NotebookFigure from '../components/ui/NotebookFigure'
import { FigureSkeleton } from '../components/ui/LoadingSkeleton'
import { useFigures } from '../hooks/useFigures'

// Static display order and grouping
const SECTIONS = [
  {
    title: 'Data Collection & Sampling',
    keys: ['01_class_distributions'],
  },
  {
    title: 'Exploratory Data Analysis',
    keys: ['02_word_count_analysis', '03_issue_breakdown'],
  },
  {
    title: 'Sentiment Preprocessing (VADER)',
    keys: ['03_vader_sentiment'],
  },
  {
    title: 'Topic Clustering (K-Means + UMAP)',
    keys: ['04_k_selection', '04_umap_visualization'],
  },
  {
    title: 'BERT Sentiment Classification',
    keys: ['05_training_history', '05_confusion_matrix'],
  },
  {
    title: 'T5 Abstractive Summarisation',
    keys: ['06_rouge_scores', '06_wordclouds'],
  },
]

export default function ResearchInsights() {
  const { data: figures, isLoading } = useFigures()

  const figureMap = figures
    ? Object.fromEntries(figures.map((f) => [f.key, f]))
    : {}

  return (
    <div className="space-y-12 animate-slide-up">
      {SECTIONS.map((section) => (
        <section key={section.title}>
          <h2 className="font-display text-[11px] text-text-muted tracking-widest uppercase mb-5">
            {section.title}
          </h2>
          <div className={`grid gap-6 ${
            section.keys.length === 1
              ? 'grid-cols-1'
              : 'grid-cols-1 xl:grid-cols-2'
          }`}>
            {section.keys.map((key) => {
              const fig = figureMap[key]
              return isLoading || !fig ? (
                <FigureSkeleton key={key} />
              ) : (
                <NotebookFigure
                  key={key}
                  figureKey={fig.key}
                  title={fig.title}
                  subtitle={fig.subtitle}
                  notebook={fig.notebook}
                  note={fig.note}
                  className={section.keys.length === 1 ? 'max-w-4xl' : ''}
                />
              )
            })}
          </div>
        </section>
      ))}
    </div>
  )
}