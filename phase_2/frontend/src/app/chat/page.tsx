"use client";

import { useAuth } from '@/lib/auth/context';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import ChatInterface from './ChatInterface';

export default function ChatPage() {
    const { user, token, isAuthenticated, isLoading: authLoading } = useAuth();
    const router = useRouter();

    // Redirect if not authenticated
    useEffect(() => {
        if (!isAuthenticated && !authLoading) {
            router.push('/login');
        }
    }, [isAuthenticated, authLoading, router]);

    if (authLoading) {
        return (
            <div className="flex justify-center items-center h-screen bg-background">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return (
            <div className="flex justify-center items-center h-screen bg-background text-foreground">
                Redirecting to login...
            </div>
        );
    }

    const userId = user?.id;
    const accessToken = token;

    if (!userId) {
        return (
            <div className="flex justify-center items-center h-screen bg-background text-foreground">
                User not found
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background pb-12">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
                <div className="mb-8">
                    <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
                        AI Assistant
                    </h1>
                    <p className="text-muted-foreground mt-2">
                        Ask questions, manage your tasks, and get intelligent insights.
                    </p>
                </div>

                <div className="glass-morphism glass-border rounded-2xl overflow-hidden shadow-2xl h-[calc(100vh-16rem)]">
                    <ChatInterface userId={userId} accessToken={accessToken || ''} />
                </div>
            </div>
        </div>
    );
}
