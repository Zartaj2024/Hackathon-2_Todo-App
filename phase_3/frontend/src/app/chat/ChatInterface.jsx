'use client';

import { useState, useEffect, useRef } from 'react';
import { FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';

export default function ChatInterface({ userId, accessToken }) {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const messagesEndRef = useRef(null);

  // Fetch conversations on component mount
  useEffect(() => {
    fetchConversations();
  }, [userId, accessToken]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchConversations = async () => {
    if (!userId || !accessToken) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/users/${userId}/chat/conversations`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setConversations(data);
      }
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading || !userId || !accessToken) return;

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
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          messages: [userMessage] // Send only the current message
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
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

      // Refresh conversations list
      fetchConversations();
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: error.message || 'Sorry, I encountered an error. Please try again.',
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

  const loadConversation = async (conversationId) => {
    if (!userId || !accessToken) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/users/${userId}/chat/conversation/${conversationId}`, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();

        // Update selected conversation
        setSelectedConversation(data.conversation);

        // Format messages to match our UI expectations
        const formattedMessages = [
          ...data.messages.map(msg => ({
            role: msg.role.toLowerCase(),
            content: msg.content,
            timestamp: msg.timestamp
          }))
        ];

        setMessages(formattedMessages);
      }
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      {/* Sidebar for conversations */}
      <div className="w-80 border-r border-gray-200 bg-gray-50">
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">Chat History</h2>
        </div>
        <div className="overflow-y-auto h-[calc(100vh-8rem)]">
          {conversations.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              No conversations yet
            </div>
          ) : (
            <div className="space-y-1 p-2">
              {conversations.map((conv) => (
                <button
                  key={conv.id}
                  onClick={() => loadConversation(conv.id)}
                  className={`w-full text-left p-3 rounded-lg hover:bg-gray-100 transition-colors ${
                    selectedConversation?.id === conv.id ? 'bg-blue-100 border border-blue-200' : ''
                  }`}
                >
                  <div className="font-medium text-gray-800 truncate">
                    {conv.title.substring(0, 30)}{conv.title.length > 30 ? '...' : ''}
                  </div>
                  <div className="text-xs text-gray-500">
                    {new Date(conv.created_at).toLocaleDateString()}
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {/* Messages area */}
        <div className="flex-1 overflow-y-auto p-6">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <FaRobot size={64} className="text-gray-300 mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">Welcome to AI Assistant</h3>
              <p className="text-gray-500 max-w-md">
                Start a conversation by typing a message below. I can help you with your tasks and answer questions.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-3xl px-4 py-3 rounded-lg ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      {message.role !== 'user' && (
                        <div className="flex-shrink-0 pt-1">
                          <FaRobot className="text-blue-500" size={18} />
                        </div>
                      )}
                      <div className="flex-1">
                        <p className="whitespace-pre-wrap">{message.content}</p>
                        {message.timestamp && (
                          <p className="text-xs opacity-70 mt-2">
                            {new Date(message.timestamp).toLocaleString()}
                          </p>
                        )}
                      </div>
                      {message.role === 'user' && (
                        <div className="flex-shrink-0 pt-1">
                          <FaUser className="text-blue-200" size={18} />
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 text-gray-800 px-4 py-3 rounded-lg max-w-3xl">
                    <div className="flex items-center space-x-3">
                      <FaRobot className="text-blue-500" size={18} />
                      <div className="animate-pulse">AI is thinking...</div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <div className="flex space-x-4">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message here... (Press Enter to send)"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows="3"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            >
              <FaPaperPlane className="mr-2" />
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}