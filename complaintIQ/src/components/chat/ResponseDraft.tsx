import { useState } from 'react'
import { Copy, Check, ChevronDown, ChevronUp } from 'lucide-react'
import type { RespondResponse } from '../../types'
import toast from 'react-hot-toast'

export default function ResponseDraft({ response }: { response: RespondResponse }) {
  const [copied, setCopied] = useState(false)
  const [collapsed, setCollapsed] = useState(false)

  const copy = async () => {
    await navigator.clipboard.writeText(response.draft_response)
    setCopied(true)
    toast.success('Response copied to clipboard')
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="w-full rounded-xl border border-emerald-500/20 bg-emerald-500/5 overflow-hidden">

      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-emerald-500/10">
        <p className="font-display text-[10px] text-emerald-400 tracking-widest uppercase">
          Draft Response · {response.response_tone}
        </p>
        <div className="flex items-center gap-2">
          <button onClick={copy} className="text-text-muted hover:text-emerald-400 transition-colors">
            {copied ? <Check size={13} /> : <Copy size={13} />}
          </button>
          <button onClick={() => setCollapsed((c) => !c)} className="text-text-muted hover:text-text-secondary transition-colors">
            {collapsed ? <ChevronDown size={13} /> : <ChevronUp size={13} />}
          </button>
        </div>
      </div>

      {/* Letter text */}
      {!collapsed && (
        <pre className="px-4 py-3 text-xs text-text-secondary font-code
                        whitespace-pre-wrap leading-relaxed max-h-64 overflow-y-auto">
          {response.draft_response}
        </pre>
      )}

      {/* Suggested actions */}
      {!collapsed && response.suggested_actions.length > 0 && (
        <div className="px-4 py-3 border-t border-emerald-500/10">
          <p className="font-display text-[10px] text-text-muted tracking-widest uppercase mb-2">
            Suggested Actions
          </p>
          <ul className="space-y-1.5">
            {response.suggested_actions.map((action, i) => (
              <li key={i} className="flex gap-2 text-xs text-text-secondary font-body">
                <span className="font-display text-emerald-400 shrink-0">{i + 1}.</span>
                {action}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}