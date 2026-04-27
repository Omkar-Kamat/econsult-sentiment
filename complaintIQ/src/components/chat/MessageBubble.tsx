import { useState } from 'react'
import { Bot, User, Zap, Loader2 } from 'lucide-react'
import type { ChatMessage } from '../../types'
import ClusterBadge from '../ui/ClusterBadge'
import SentimentBadge from '../ui/SentimentBadge'
import ResponseDraft from './ResponseDraft'

interface MessageBubbleProps {
  message: ChatMessage
  onGenerateResponse: (id: string, name: string, agent: string) => void
  isResponding: boolean
}

export default function MessageBubble({ message, onGenerateResponse, isResponding }: MessageBubbleProps) {
  const isUser = message.role === 'user'
  const [name, setName] = useState('Valued Customer')
  const [agent, setAgent] = useState('Customer Relations Team')
  const [showForm, setShowForm] = useState(false)

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>

      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0
                       ${isUser ? 'bg-accent/20 text-accent' : 'bg-bg-raised text-text-secondary'}`}>
        {isUser ? <User size={15} /> : <Bot size={15} />}
      </div>

      {/* Content */}
      <div className={`flex flex-col gap-2 max-w-[85%] ${isUser ? 'items-end' : 'items-start'}`}>

        {/* Main bubble */}
        <div className={`px-4 py-3 rounded-xl text-sm font-body leading-relaxed
                         ${isUser
                           ? 'bg-accent/10 border border-accent/20 text-text-primary'
                           : 'bg-bg-raised border border-border text-text-secondary'}`}>
          {message.content || (message.classification ? null : '...')}
        </div>

        {/* Classification result */}
        {message.classification && (
          <div className="bg-bg-raised border border-border rounded-xl p-4 space-y-3 w-full">
            <p className="font-display text-[10px] text-text-muted tracking-widest uppercase">
              Classification Result
            </p>
            <div className="flex flex-wrap gap-2">
              <ClusterBadge
                clusterId={message.classification.cluster_id}
                label={message.classification.cluster_label}
              />
              <SentimentBadge
                sentiment={message.classification.sentiment}
                confidence={message.classification.sentiment_scores[message.classification.sentiment]}
              />
            </div>
            <p className="font-display text-[11px] text-text-muted">
              Product hint: {message.classification.product_hint}
              <span className="ml-3">· {message.classification.processing_ms}ms</span>
            </p>

            {/* Generate response trigger */}
            {!message.response && (
              <div className="pt-1 border-t border-border space-y-2">
                {showForm ? (
                  <div className="space-y-2">
                    <input
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      placeholder="Customer name"
                      className="w-full bg-bg border border-border rounded-lg px-3 py-1.5
                                 text-xs text-text-primary placeholder:text-text-muted
                                 font-body focus:outline-none focus:border-border-active"
                    />
                    <input
                      value={agent}
                      onChange={(e) => setAgent(e.target.value)}
                      placeholder="Agent name"
                      className="w-full bg-bg border border-border rounded-lg px-3 py-1.5
                                 text-xs text-text-primary placeholder:text-text-muted
                                 font-body focus:outline-none focus:border-border-active"
                    />
                    <button
                      onClick={() => onGenerateResponse(message.classification!.complaint_id, name, agent)}
                      disabled={isResponding}
                      className="w-full flex items-center justify-center gap-2 bg-accent text-bg
                                 text-xs font-display tracking-wide rounded-lg py-2
                                 hover:bg-amber-400 disabled:opacity-50 transition-all"
                    >
                      {isResponding
                        ? <><Loader2 size={12} className="animate-spin" /> Generating...</>
                        : <><Zap size={12} /> Generate Response</>
                      }
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowForm(true)}
                    className="text-accent font-display text-[11px] tracking-wide
                               hover:text-amber-400 transition-colors"
                  >
                    + Generate Response →
                  </button>
                )}
              </div>
            )}
          </div>
        )}

        {/* Response draft */}
        {message.response && <ResponseDraft response={message.response} />}
      </div>
    </div>
  )
}