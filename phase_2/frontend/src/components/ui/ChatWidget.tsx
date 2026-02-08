'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/lib/auth/context';
import { FaComment, FaTimes, FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';
import { Button } from '@/components/ui/Button';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
}

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { user, token, isAuthenticated, isLoading: authIsLoading } = useAuth();
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const userId = user?.id;

    useEffect(() => {
        if (isOpen) {
            scrollToBottom();
        }
    }, [messages, isOpen]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const toggleChat = () => setIsOpen(!isOpen);

    const sendMessage = async () => {
        if (!inputValue.trim() || !userId || isLoading || !isAuthenticated) return;

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
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    messages: [userMessage]
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.messages && data.messages.length > 0) {
                setMessages(prev => [...prev, ...data.messages.map((msg: any) => ({
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

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    if (authIsLoading || !isAuthenticated) {
        return null;
    }

    return (
        <>
            {!isOpen && (
                <button
                    onClick={toggleChat}
                    className="fixed bottom-8 right-8 bg-gradient-to-br from-primary to-primary-700 text-white p-5 rounded-full shadow-primary-glow hover:scale-110 transition-all duration-300 z-50 animate-float"
                    aria-label="Open chat"
                >
                    <FaComment size={24} />
                    <div className="absolute -top-1 -right-1 w-4 h-4 bg-secondary rounded-full border-2 border-background animate-pulse"></div>
                </button>
            )}

            {isOpen && (
                <div className="fixed bottom-8 right-8 w-[400px] h-[600px] flex flex-col glass-morphism glass-border rounded-3xl shadow-2xl z-50 animate-fade-in overflow-hidden">
                    <div className="bg-gradient-to-r from-primary to-primary-700 text-white p-5 flex justify-between items-center shadow-lg">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                                <FaRobot className="text-white" size={20} />
                            </div>
                            <div>
                                <h3 className="font-bold">AI Assistant</h3>
                                <p className="text-[10px] text-primary-200 uppercase tracking-widest">Online</p>
                            </div>
                        </div>
                        <button
                            onClick={toggleChat}
                            className="w-8 h-8 rounded-full hover:bg-white/20 flex items-center justify-center transition-colors"
                            aria-label="Close chat"
                        >
                            <FaTimes />
                        </button>
                    </div>

                    <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-transparent custom-scrollbar">
                        {messages.length === 0 ? (
                            <div className="text-center text-muted-foreground/60 mt-12">
                                <FaRobot size={48} className="mx-auto mb-4 text-primary/20" />
                                <p className="font-medium">How can I help you with your tasks today?</p>
                            </div>
                        ) : (
                            messages.map((message, index) => (
                                <div
                                    key={index}
                                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
                                >
                                    <div
                                        className={`max-w-[80%] px-4 py-3 rounded-2xl shadow-sm ${message.role === 'user'
                                                ? 'bg-primary text-white rounded-tr-none'
                                                : 'bg-white/10 glass-border text-foreground rounded-tl-none'
                                            }`}
                                    >
                                        <div className="flex items-start space-x-2">
                                            <div>
                                                <p className="text-sm leading-relaxed">{message.content}</p>
                                                {message.timestamp && (
                                                    <p className="text-[10px] opacity-50 mt-1">
                                                        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                                    </p>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                        {isLoading && (
                            <div className="flex justify-start animate-fade-in">
                                <div className="bg-white/10 glass-border text-foreground px-4 py-3 rounded-2xl rounded-tl-none shadow-sm">
                                    <div className="flex space-x-2">
                                        <div className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce"></div>
                                        <div className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                                        <div className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="p-5 border-t border-border/50 bg-background/50 backdrop-blur-md">
                        <div className="flex items-end space-x-3">
                            <textarea
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyDown={handleKeyPress}
                                placeholder="Type a message..."
                                className="flex-1 glass-morphism glass-border rounded-xl px-4 py-2 resize-none focus:outline-none focus:ring-1 focus:ring-primary/30 text-sm bg-white/5"
                                rows={1}
                                disabled={isLoading}
                            />
                            <Button
                                onClick={sendMessage}
                                disabled={isLoading || !inputValue.trim()}
                                variant="premium"
                                className="h-10 w-10 p-0 rounded-xl shadow-primary-glow"
                            >
                                <FaPaperPlane size={14} />
                            </Button>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
