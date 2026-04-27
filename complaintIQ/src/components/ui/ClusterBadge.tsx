import { clsx } from 'clsx'

const CLUSTER_STYLES: Record<number, string> = {
  0: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  1: 'bg-violet-500/10 text-violet-400 border-violet-500/20',
  2: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
}

interface ClusterBadgeProps {
  clusterId: 0 | 1 | 2
  label: string
  size?: 'sm' | 'md'
}

export default function ClusterBadge({
  clusterId, label, size = 'md',
}: ClusterBadgeProps) {
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full border font-display tracking-wide',
        CLUSTER_STYLES[clusterId],
        size === 'sm' ? 'text-[10px] px-2 py-0.5' : 'text-xs px-2.5 py-1'
      )}
    >
      <span className={clsx(
        'rounded-full mr-1.5',
        size === 'sm' ? 'w-1 h-1' : 'w-1.5 h-1.5',
        clusterId === 0 ? 'bg-blue-400' :
        clusterId === 1 ? 'bg-violet-400' : 'bg-amber-400'
      )} />
      {label}
    </span>
  )
}