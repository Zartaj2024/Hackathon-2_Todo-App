'use client';

import { useState, useEffect, useRef } from 'react';
import { FaPaperPlane, FaRobot, FaUser, FaHistory, FaPlus } from 'react-icons/fa';
import { Button } from '@/components/ui/Button';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
}

interface Conversation {
    id: string;
    title: string;
    created_at: string;
}

interface ChatInterfaceProps {
    userId: string;
    accessToken: string;
}

export default function ChatInterface({ userId, accessToken }: ChatInterfaceProps) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        fetchConversations();
    }, [userId, accessToken]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const fetchConversations = async () => {
        if (!userId || !accessToken) return;

        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
            const response = await fetch(`${baseUrl}/users/${userId}/chat/conversations`, {
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

    const startNewChat = () => {
        setMessages([]);
        setSelectedConversation(null);
        setInputValue('');
    };

    const sendMessage = async () => {
        if (!inputValue.trim() || isLoading || !userId || !accessToken) return;

        const userMessage: Message = {
            role: 'user',
            content: inputValue,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
            const response = await fetch(`${baseUrl}/users/${userId}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    messages: [userMessage]
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.messages && data.messages.length > 0) {
                setMessages(prev => [...prev, ...data.messages.map((msg: any) => ({
                    ...msg,
                    role: msg.role || 'assistant',
                    timestamp: msg.timestamp || new Date().toISOString()
                }))]);
            }

            fetchConversations();
        } catch (error: any) {
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

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const loadConversation = async (conversationId: string) => {
        if (!userId || !accessToken) return;

        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
            const response = await fetch(`${baseUrl}/users/${userId}/chat/conversation/${conversationId}`, {
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const data = await response.json();
                setSelectedConversation(data.conversation);
                const formattedMessages = data.messages.map((msg: any) => ({
                    role: msg.role.toLowerCase(),
                    content: msg.content,
                    timestamp: msg.timestamp
                }));
                setMessages(formattedMessages);
            }
        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    };

    return (
        <div className="flex h-full bg-transparent overflow-hidden">
            <div className="w-80 border-r border-border/50 bg-background/30 backdrop-blur-md flex flex-col hidden md:flex">
                <div className="p-4 border-b border-border/50 flex justify-between items-center">
                    <h2 className="text-lg font-semibold flex items-center gap-2">
                        <FaHistory className="text-primary/70" />
                        History
                    </h2>
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={startNewChat}
                        className="hover:bg-primary/10 rounded-full"
                    >
                        <FaPlus />
                    </Button>
                </div>
                <div className="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-2">
                    {conversations.length === 0 ? (
                        <div className="p-8 text-center text-muted-foreground/60 text-sm italic">
                            No chat history yet
                        </div>
                    ) : (
                        conversations.map((conv) => (
                            <button
                                key={conv.id}
                                onClick={() => loadConversation(conv.id)}
                                className={`w-full text-left p-3 rounded-xl transition-all duration-200 group ${selectedConversation?.id === conv.id
                                        ? 'bg-primary/20 border border-primary/30 shadow-lg'
                                        : 'hover:bg-white/5 border border-transparent underline-none'
                                    }`}
                            >
                                <div className={`font-medium truncate ${selectedConversation?.id === conv.id ? 'text-primary' : 'text-foreground/80'}`}>
                                    {conv.title}
                                </div>
                                <div className="text-[10px] text-muted-foreground mt-1 uppercase tracking-wider">
                                    {new Date(conv.created_at).toLocaleDateString()}
                                </div>
                            </button>
                        ))
                    )}
                </div>
            </div>

            <div className="flex-1 flex flex-col bg-transparent">
                <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                    {messages.length === 0 ? (
                        <div className="flex flex-col items-center justify-center h-full text-center">
                            <div className="relative mb-6">
                                <div className="absolute inset-0 bg-primary/20 blur-3xl rounded-full animate-pulse"></div>
                                <FaRobot size={80} className="text-primary relative z-10" />
                            </div>
                            <h3 className="text-2xl font-bold mb-2">How can I help you today?</h3>
                            <p className="text-muted-foreground max-w-sm">
                                I can help you manage your tasks, prioritize your day, or just chat.
                            </p>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            {messages.map((message, index) => (
                                <div
                                    key={index}
                                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
                                >
                                    <div className={`flex gap-3 max-w-[85%] ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg ${message.role === 'user' ? 'bg-primary text-white' : 'bg-secondary text-white'
                                            }`}>
                                            {message.role === 'user' ? <FaUser size={14} /> : <FaRobot size={14} />}
                                        </div>
                                        <div className={`px-5 py-3 rounded-2xl shadow-xl ${message.role === 'user'
                                                ? 'bg-gradient-to-br from-primary to-primary-600 text-white rounded-tr-none'
                                                : 'glass-morphism glass-border text-foreground rounded-tl-none'
                                            }`}>
                                            <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>
                                            {message.timestamp && (
                                                <div className={`text-[10px] mt-2 opacity-50 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                                                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="flex justify-start animate-fade-in">
                                    <div className="flex gap-3 max-w-[85%]">
                                        <div className="w-8 h-8 rounded-full bg-secondary text-white flex items-center justify-center flex-shrink-0 animate-pulse">
                                            <FaRobot size={14} />
                                        </div>
                                        <div className="glass-morphism glass-border px-5 py-3 rounded-2xl shadow-xl rounded-tl-none">
                                            <div className="flex space-x-2">
                                                <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                                                <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                                                <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>
                    )}
                </div>

                <div className="p-6 border-t border-border/50 bg-background/50 backdrop-blur-md">
                    <div className="relative flex items-end gap-3 max-w-4xl mx-auto">
                        <textarea
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={handleKeyPress}
                            placeholder="Ask anything..."
                            className="flex-1 glass-morphism glass-border rounded-2xl px-5 py-4 min-h-[56px] max-h-32 resize-none focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all shadow-inner text-foreground placeholder:text-muted-foreground/50"
                            rows={1}
                            disabled={isLoading}
                        />
                        <Button
                            onClick={sendMessage}
                            disabled={isLoading || !inputValue.trim()}
                            variant="premium"
                            className="h-14 w-14 rounded-2xl p-0 flex items-center justify-center shadow-primary-glow"
                        >
                            <FaPaperPlane size={18} />
                        </Button>
                    </div>
                    <div className="text-[10px] text-center mt-3 text-muted-foreground/40 font-medium uppercase tracking-[0.2em]">
                        AI Assistant may provide inaccurate info.
                    </div>
                </div>
            </div>
        </div>
    );
}
