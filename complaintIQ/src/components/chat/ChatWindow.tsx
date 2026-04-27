import { useState, useRef, useEffect } from 'react'
import { Send, Loader2 } from 'lucide-react'
import type { ChatMessage } from '../../types'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'

interface ChatWindowProps {
  messages: ChatMessage[]
  onSubmit: (text: string) => void
  onGenerateResponse: (id: string, name: string, agent: string) => void
  isClassifying: boolean
  isResponding: boolean
}

export default function ChatWindow({
  messages, onSubmit, onGenerateResponse, isClassifying, isResponding,
}: ChatWindowProps) {
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = () => {
    if (!input.trim() || isClassifying) return
    onSubmit(input.trim())
    setInput('')
  }

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full rounded-xl border border-border bg-bg-surface overflow-hidden">

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-5 py-5 space-y-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-center">
            <div>
              <p className="font-display text-text-muted text-sm tracking-wide">
                PASTE A COMPLAINT TO BEGIN
              </p>
              <p className="font-body text-xs text-text-muted mt-1">
                The AI will classify it by cluster and sentiment, then draft a response.
              </p>
            </div>
          </div>
        )}

        {messages.map((msg) => (
          msg.isLoading ? (
            <TypingIndicator key={msg.id} />
          ) : (
            <MessageBubble
              key={msg.id}
              message={msg}
              onGenerateResponse={onGenerateResponse}
              isResponding={isResponding}
            />
          )
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t border-border p-4">
        <div className="flex gap-3 items-end">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Paste complaint narrative here..."
            rows={3}
            className="flex-1 resize-none bg-bg-raised border border-border rounded-lg
                       px-4 py-3 text-sm text-text-primary placeholder:text-text-muted
                       font-body focus:outline-none focus:border-border-active
                       transition-colors"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isClassifying}
            className="w-11 h-11 rounded-lg bg-accent text-bg flex items-center justify-center
                       hover:bg-amber-400 disabled:opacity-40 disabled:cursor-not-allowed
                       transition-all shrink-0"
          >
            {isClassifying
              ? <Loader2 size={18} className="animate-spin" />
              : <Send size={18} />
            }
          </button>
        </div>
        <p className="font-display text-[10px] text-text-muted mt-2 tracking-wide">
          ENTER to send · SHIFT+ENTER for new line
        </p>
      </div>
    </div>
  )
}