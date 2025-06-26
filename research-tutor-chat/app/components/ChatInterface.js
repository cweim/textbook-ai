// app/components/ChatInterface.js
'use client';

import { useState, useRef, useEffect } from 'react';
import { Send, BookOpen, MessageCircle, AlertCircle } from 'lucide-react';

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your Research Methods tutor. Ask me anything about the textbook, or I can help create quizzes and study materials for you! 📚',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage.content }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      const assistantMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        tokensUsed: data.tokensUsed
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);

      // Add error message to chat
      const errorMessage = {
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const clearChat = () => {
    setMessages([{
      role: 'assistant',
      content: 'Chat cleared! How can I help you with Research Methods today?',
      timestamp: new Date()
    }]);
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto bg-white">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <BookOpen className="h-8 w-8" />
            <div>
              <h1 className="text-2xl font-bold">Research Methods Tutor</h1>
              <p className="text-blue-100 text-sm">Your AI assistant for "Research Methods for Business Students"</p>
            </div>
          </div>
          <button
            onClick={clearChat}
            className="px-3 py-1 bg-blue-500 hover:bg-blue-400 rounded-lg text-sm transition-colors"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-red-500" />
          <span className="text-red-700">{error}</span>
          <button
            onClick={() => setError('')}
            className="ml-auto text-red-500 hover:text-red-700"
          >
            ×
          </button>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] ${msg.role === 'user' ? 'order-2' : 'order-1'}`}>
              <div className={`p-4 rounded-lg shadow-sm ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white rounded-br-sm'
                  : msg.isError
                  ? 'bg-red-100 text-red-800 border border-red-200 rounded-bl-sm'
                  : 'bg-white text-gray-800 border border-gray-200 rounded-bl-sm'
              }`}>
                <div className="whitespace-pre-wrap">{msg.content}</div>
                <div className={`text-xs mt-2 ${
                  msg.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                  {formatTime(msg.timestamp)}
                  {msg.tokensUsed && (
                    <span className="ml-2">• {msg.tokensUsed} tokens</span>
                  )}
                </div>
              </div>
            </div>
            <div className={`flex items-end p-2 ${msg.role === 'user' ? 'order-1' : 'order-2'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-300 text-gray-700'
              }`}>
                {msg.role === 'user' ? 'U' : '🤖'}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent"></div>
                <span className="text-gray-600">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about research methods, request quizzes, or get study help..."
              className="w-full border border-gray-300 rounded-lg px-4 py-3 pr-12 resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows="1"
              disabled={loading}
              style={{ minHeight: '50px', maxHeight: '120px' }}
              onInput={(e) => {
                e.target.style.height = 'auto';
                e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
              }}
            />
            <div className="absolute right-3 bottom-3 text-gray-400 text-xs">
              {input.length}/1000
            </div>
          </div>
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim() || input.length > 1000}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white p-3 rounded-lg transition-colors flex items-center justify-center min-w-[50px]"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>

        {/* Quick Actions */}
        <div className="flex gap-2 mt-3 flex-wrap">
          {[
            "What is a research proposal?",
            "Create a quiz on data collection",
            "Explain qualitative vs quantitative research",
            "Help me understand sampling methods"
          ].map((suggestion, idx) => (
            <button
              key={idx}
              onClick={() => setInput(suggestion)}
              className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm transition-colors"
              disabled={loading}
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
