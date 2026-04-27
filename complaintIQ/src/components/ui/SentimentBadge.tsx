import { clsx } from 'clsx'
import { TrendingDown, Minus, TrendingUp } from 'lucide-react'

const STYLES = {
  negative: 'bg-red-500/10 text-red-400 border-red-500/20',
  neutral:  'bg-gray-500/10 text-gray-400 border-gray-500/20',
  positive: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
}

const ICONS = {
  negative: TrendingDown,
  neutral:  Minus,
  positive: TrendingUp,
}

interface SentimentBadgeProps {
  sentiment: 'negative' | 'neutral' | 'positive'
  confidence?: number
}

export default function SentimentBadge({ sentiment, confidence }: SentimentBadgeProps) {
  const Icon = ICONS[sentiment]
  return (
    <span className={clsx(
      'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border',
      'font-display text-xs tracking-wide',
      STYLES[sentiment]
    )}>
      <Icon size={11} />
      {sentiment}
      {confidence !== undefined && (
        <span className="opacity-60">{Math.round(confidence * 100)}%</span>
      )}
    </span>
  )
}