import { clsx } from 'clsx'
import type { LucideIcon } from 'lucide-react'

interface StatCardProps {
  label: string
  value: string | number
  sub?: string
  icon: LucideIcon
  accent?: boolean
  trend?: 'up' | 'down' | 'neutral'
}

export default function StatCard({
  label, value, sub, icon: Icon, accent = false, trend,
}: StatCardProps) {
  return (
    <div
      className={clsx(
        'relative rounded-xl border p-5 transition-all duration-200',
        accent
          ? 'bg-accent-glow border-accent/30'
          : 'bg-bg-surface border-border hover:border-border-active'
      )}
    >
      {/* Icon */}
      <div
        className={clsx(
          'w-9 h-9 rounded-lg flex items-center justify-center mb-4',
          accent ? 'bg-accent/20' : 'bg-bg-raised'
        )}
      >
        <Icon size={18} className={accent ? 'text-accent' : 'text-text-secondary'} />
      </div>

      {/* Value */}
      <p className={clsx(
        'font-display text-2xl font-medium tracking-tight',
        accent ? 'text-accent' : 'text-text-primary'
      )}>
        {value}
      </p>

      {/* Label */}
      <p className="font-body text-xs text-text-secondary mt-1">{label}</p>

      {/* Sub */}
      {sub && (
        <p className="font-display text-[11px] text-text-muted mt-2 tracking-wide">
          {sub}
        </p>
      )}
    </div>
  )
}