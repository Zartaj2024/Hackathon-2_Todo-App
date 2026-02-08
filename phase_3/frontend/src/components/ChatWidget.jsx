'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth/context';
import { FaComment, FaTimes, FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { user, token, isAuthenticated, isLoading: authIsLoading } = useAuth();

  // Extract user ID from the custom auth context
  const userId = user?.id;

  const toggleChat = () => setIsOpen(!isOpen);

  const sendMessage = async () => {
    if (!inputValue.trim() || !userId || isLoading || !isAuthenticated) return;

    const userMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    // Add user message to UI immediately
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/users/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          messages: [userMessage] // Send only the new message, not all messages
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add assistant response to messages
      if (data.messages && data.messages.length > 0) {
        setMessages(prev => [...prev, ...data.messages.map(msg => ({
          ...msg,
          role: msg.role || 'assistant',
          timestamp: msg.timestamp || new Date().toISOString()
        }))]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Show nothing if not authenticated
  if (authIsLoading) {
    return null; // Don't render anything while loading
  }

  if (!isAuthenticated) {
    return null; // Don't render if not authenticated
  }

  return (
    <>
      {/* Chat Widget Button */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-colors z-50"
          aria-label="Open chat"
        >
          <FaComment size={20} />
        </button>
      )}

      {/* Chat Widget Container */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-full max-w-md h-[600px] flex flex-col bg-white rounded-lg shadow-xl border border-gray-200 z-50">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <FaRobot className="text-blue-200" />
              <h3 className="font-semibold">AI Assistant</h3>
            </div>
            <button
              onClick={toggleChat}
              className="text-white hover:text-blue-200 transition-colors"
              aria-label="Close chat"
            >
              <FaTimes />
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 mt-8">
                <FaRobot size={48} className="mx-auto mb-4 text-gray-300" />
                <p>Start a conversation with our AI assistant!</p>
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-800'
                    }`}
                  >
                    <div className="flex items-start space-x-2">
                      {message.role !== 'user' && (
                        <FaRobot className="mt-1 text-gray-600" size={14} />
                      )}
                      <div>
                        <p>{message.content}</p>
                        {message.timestamp && (
                          <p className="text-xs opacity-70 mt-1">
                            {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        )}
                      </div>
                      {message.role === 'user' && (
                        <FaUser className="mt-1 text-blue-200" size={14} />
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg max-w-xs">
                  <div className="flex items-center space-x-2">
                    <FaRobot className="text-gray-600" size={14} />
                    <div className="animate-pulse">AI is thinking...</div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4 bg-white">
            <div className="flex space-x-2">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="flex-1 border border-gray-300 rounded-lg px-3 py-2 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="2"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                aria-label="Send message"
              >
                <FaPaperPlane />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}