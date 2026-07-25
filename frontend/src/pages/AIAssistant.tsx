import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Sprout, Activity, RefreshCw } from 'lucide-react';
import { assistantService, ChatMessage } from '../api/assistant.service';

const QUICK_ACTIONS = [
  { text: "What were my recent disease scans?", icon: <Activity className="w-4 h-4" /> },
  { text: "I need a fertilizer plan", icon: <Sprout className="w-4 h-4" /> },
  { text: "How do I treat Apple Scab?", icon: <RefreshCw className="w-4 h-4" /> },
];

export const AIAssistant: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([{
    role: 'assistant',
    content: "Hello! I am Rutu, your AI Farming Assistant. I can help you analyze your recent crop scans, explain fertilizer recommendations, or answer general questions about crop diseases."
  }]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    // Add user message
    const userMsg: ChatMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await assistantService.sendMessage(text, sessionId);
      if (!sessionId) {
        setSessionId(response.session_id);
      }
      const assistantMsg: ChatMessage = { role: 'assistant', content: response.message };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, { role: 'system', content: 'Failed to connect to the assistant. Please try again later.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] animate-fade-in">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
          <Bot className="w-7 h-7 text-emerald-600" />
          Rutu
        </h1>
        <p className="text-slate-500">Ask me anything about your farm, crops, or recent AI predictions.</p>
      </div>

      <div className="flex-1 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
        
        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 bg-slate-50">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0 border border-emerald-200">
                  <Bot className="w-5 h-5 text-emerald-700" />
                </div>
              )}
              
              <div className={`max-w-[80%] rounded-2xl px-5 py-3 ${
                msg.role === 'user' 
                  ? 'bg-emerald-600 text-white rounded-br-none shadow-md shadow-emerald-200' 
                  : msg.role === 'system'
                  ? 'bg-red-50 text-red-700 border border-red-200 text-sm'
                  : 'bg-white text-slate-700 border border-slate-200 rounded-bl-none shadow-sm'
              }`}>
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center flex-shrink-0">
                  <User className="w-5 h-5 text-slate-600" />
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="flex gap-4 justify-start">
              <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-4 h-4 text-emerald-700 animate-spin" />
              </div>
              <div className="bg-white border border-slate-200 rounded-2xl rounded-bl-none px-5 py-3 shadow-sm flex gap-1 items-center">
                <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-slate-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Actions */}
        {messages.length === 1 && !isLoading && (
          <div className="px-4 py-3 bg-white border-t border-slate-100 flex flex-wrap gap-2">
            {QUICK_ACTIONS.map((action, idx) => (
              <button 
                key={idx}
                onClick={() => handleSend(action.text)}
                className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 hover:bg-emerald-50 text-slate-600 hover:text-emerald-700 text-sm rounded-full border border-slate-200 hover:border-emerald-200 transition-colors"
              >
                {action.icon}
                {action.text}
              </button>
            ))}
          </div>
        )}

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-slate-200">
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSend(input); }}
            className="flex gap-3"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything about your farm..."
              className="flex-1 rounded-lg border border-slate-300 px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-shadow"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-300 text-white px-5 py-2.5 rounded-lg flex items-center justify-center transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <div className="text-center mt-2">
            <p className="text-[10px] text-slate-400">
              AI Assistant can make mistakes. Verify critical treatment plans with agricultural experts.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
