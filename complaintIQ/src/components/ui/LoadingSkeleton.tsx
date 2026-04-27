import { clsx } from 'clsx'

interface SkeletonProps {
  className?: string
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={clsx(
        'animate-pulse rounded bg-bg-raised',
        className
      )}
    />
  )
}

export function StatCardSkeleton() {
  return (
    <div className="rounded-xl border border-border bg-bg-surface p-5 space-y-3">
      <Skeleton className="w-9 h-9 rounded-lg" />
      <Skeleton className="h-7 w-24" />
      <Skeleton className="h-3 w-32" />
    </div>
  )
}

export function FigureSkeleton() {
  return (
    <div className="rounded-xl border border-border bg-bg-surface overflow-hidden">
      <div className="p-5 border-b border-border space-y-2">
        <Skeleton className="h-3 w-24" />
        <Skeleton className="h-4 w-48" />
        <Skeleton className="h-3 w-64" />
      </div>
      <Skeleton className="h-56 w-full rounded-none" />
    </div>
  )
}