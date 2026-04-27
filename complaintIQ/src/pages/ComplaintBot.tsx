import { useState } from 'react'
import { useClassify } from '../hooks/useClassify'
import { useRespond } from '../hooks/useRespond'
import type { ChatMessage, ClassifyResponse, RespondResponse } from '../types'
import ChatWindow from '../components/chat/ChatWindow'
import ContextPanel from '../components/chat/ContextPanel'
import toast from 'react-hot-toast'

export default function ComplaintBot() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [lastClassification, setLastClassification] = useState<ClassifyResponse | null>(null)
  const [lastResponse, setLastResponse] = useState<RespondResponse | null>(null)

  const classify = useClassify()
  const respond = useRespond()

  const addMessage = (msg: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    setMessages((prev) => [
      ...prev,
      { ...msg, id: crypto.randomUUID(), timestamp: new Date() },
    ])
  }

  const handleSubmitComplaint = async (text: string) => {
    addMessage({ role: 'user', content: text })

    const loadingId = crypto.randomUUID()
    setMessages((prev) => [
      ...prev,
      { id: loadingId, role: 'bot', content: '', timestamp: new Date(), isLoading: true },
    ])

    try {
      const result = await classify.mutateAsync({ complaint_text: text })
      setLastClassification(result)

      setMessages((prev) =>
        prev.map((m) =>
          m.id === loadingId
            ? { ...m, isLoading: false, content: 'Complaint classified.', classification: result }
            : m
        )
      )
    } catch (err) {
      setMessages((prev) => prev.filter((m) => m.id !== loadingId))
      toast.error('Classification failed. Is the backend running?')
    }
  }

  const handleGenerateResponse = async (
    complaintId: string,
    customerName: string,
    agentName: string
  ) => {
    const loadingId = crypto.randomUUID()
    setMessages((prev) => [
      ...prev,
      { id: loadingId, role: 'bot', content: '', timestamp: new Date(), isLoading: true },
    ])

    try {
      const result = await respond.mutateAsync({
        complaint_id: complaintId,
        customer_name: customerName,
        agent_name: agentName,
      })
      setLastResponse(result)

      setMessages((prev) =>
        prev.map((m) =>
          m.id === loadingId
            ? { ...m, isLoading: false, content: 'Response generated.', response: result }
            : m
        )
      )
    } catch (err) {
      setMessages((prev) => prev.filter((m) => m.id !== loadingId))
      toast.error('Response generation failed.')
    }
  }

  return (
    <div className="flex gap-6 h-[calc(100vh-8rem)] animate-fade-in">
      {/* Left — Chat */}
      <div className="flex flex-col flex-1 min-w-0">
        <ChatWindow
          messages={messages}
          onSubmit={handleSubmitComplaint}
          onGenerateResponse={handleGenerateResponse}
          isClassifying={classify.isPending}
          isResponding={respond.isPending}
        />
      </div>

      {/* Right — Context */}
      <div className="w-96 shrink-0">
        <ContextPanel
          classification={lastClassification}
          response={lastResponse}
        />
      </div>
    </div>
  )
}