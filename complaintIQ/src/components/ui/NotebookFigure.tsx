import { useState } from 'react'
import { getFigureUrl } from '../../api/client'
import { BookOpen, ZoomIn } from 'lucide-react'

interface NotebookFigureProps {
  figureKey: string
  title: string
  subtitle: string
  notebook: string
  note?: string
  className?: string
}

export default function NotebookFigure({
  figureKey, title, subtitle, notebook, note, className = '',
}: NotebookFigureProps) {
  const [loaded, setLoaded] = useState(false)
  const [zoomed, setZoomed] = useState(false)
  const url = getFigureUrl(figureKey)

  return (
    <>
      <div
        className={`rounded-xl border border-border bg-bg-surface overflow-hidden
                    hover:border-border-active transition-all duration-200 ${className}`}
      >
        {/* Card header */}
        <div className="px-5 py-4 border-b border-border">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <BookOpen size={14} className="text-accent" />
              <span className="font-display text-[11px] text-accent tracking-widest uppercase">
                {notebook}
              </span>
            </div>
            <button
              onClick={() => setZoomed(true)}
              className="text-text-muted hover:text-text-secondary transition-colors"
              title="View full size"
            >
              <ZoomIn size={14} />
            </button>
          </div>
          <h3 className="font-body text-sm font-semibold text-text-primary mt-2">
            {title}
          </h3>
          <p className="font-body text-xs text-text-secondary mt-0.5 leading-relaxed">
            {subtitle}
          </p>
        </div>

        {/* Image */}
        <div className="relative bg-bg-raised">
          {!loaded && (
            <div className="absolute inset-0 flex items-center justify-center h-48">
              <div className="w-6 h-6 border-2 border-accent/30 border-t-accent
                              rounded-full animate-spin" />
            </div>
          )}
          <img
            src={url}
            alt={title}
            className={`w-full object-contain max-h-72 transition-opacity duration-300
                        cursor-zoom-in ${loaded ? 'opacity-100' : 'opacity-0'}`}
            onLoad={() => setLoaded(true)}
            onClick={() => setZoomed(true)}
          />
        </div>

        {/* Methodology note */}
        {note && (
          <div className="px-5 py-3 border-t border-border bg-bg-raised/50">
            <p className="font-body text-[11px] text-text-muted leading-relaxed">
              <span className="text-accent font-medium">Note: </span>
              {note}
            </p>
          </div>
        )}
      </div>

      {/* Full-size zoom modal */}
      {zoomed && (
        <div
          className="fixed inset-0 z-50 bg-bg/90 backdrop-blur-sm flex items-center
                     justify-center p-8 animate-fade-in cursor-zoom-out"
          onClick={() => setZoomed(false)}
        >
          <img
            src={url}
            alt={title}
            className="max-w-full max-h-full object-contain rounded-xl shadow-2xl"
          />
        </div>
      )}
    </>
  )
}