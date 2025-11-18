'use client'

import { useState } from 'react'
import api from '../../../lib/api'

export default function AICopilotPage() {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.post('/api/ai/copilot', {
        messages: [...messages, userMessage]
      })
      
      setMessages([...messages, userMessage, {
        role: 'assistant',
        content: response.data.message || response.data.error || 'No response'
      }])
    } catch (error) {
      setMessages([...messages, userMessage, {
        role: 'assistant',
        content: 'Error: Could not get response from AI Copilot'
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-[calc(100vh-120px)] flex flex-col">
      <h1 className="text-3xl font-bold mb-6">AI Copilot</h1>
      <div className="flex-1 card-stripe p-6 flex flex-col">
        <div className="flex-1 overflow-y-auto mb-4 space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`p-4 rounded-lg ${
                msg.role === 'user'
                  ? 'bg-stripe-blue text-white ml-auto max-w-[80%]'
                  : 'bg-slate-100 max-w-[80%]'
              }`}
            >
              {msg.content}
            </div>
          ))}
          {loading && (
            <div className="bg-slate-100 p-4 rounded-lg max-w-[80%]">
              Thinking...
            </div>
          )}
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            className="input-stripe flex-1"
            placeholder="Ask me anything about markets, portfolios, or analysis..."
          />
          <button onClick={sendMessage} className="btn-stripe">
            Send
          </button>
        </div>
      </div>
    </div>
  )
}
