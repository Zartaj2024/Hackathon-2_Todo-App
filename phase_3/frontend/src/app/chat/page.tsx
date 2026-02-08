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
      <div className="flex justify-center items-center h-screen">
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="flex justify-center items-center h-screen">
        Redirecting to login...
      </div>
    );
  }

  // Get the user ID and token from the auth context
  const userId = user?.id;
  const accessToken = token;

  if (!userId) {
    return (
      <div className="flex justify-center items-center h-screen">
        User not found
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <ChatInterface userId={userId} accessToken={accessToken} />
        </div>
      </div>
    </div>
  );
}