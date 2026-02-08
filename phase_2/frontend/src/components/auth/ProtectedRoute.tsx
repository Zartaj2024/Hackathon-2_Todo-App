'use client';

import React, { useEffect } from 'react';
import { useAuth } from '@/lib/auth/context';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/Card';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = (
    <Card className="w-full max-w-md mx-auto mt-20">
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Checking authentication...</p>
      </div>
    </Card>
  )
}) => {
  const { isAuthenticated, isLoading, token } = useAuth();
  const router = useRouter();

  console.log('ProtectedRoute: Auth state - isLoading:', isLoading, 'isAuthenticated:', isAuthenticated, 'token:', token ? 'PRESENT' : 'MISSING');

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      console.log('ProtectedRoute: User not authenticated, redirecting to login');
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    console.log('ProtectedRoute: Still loading, showing fallback');
    return fallback;
  }

  if (!isAuthenticated) {
    console.log('ProtectedRoute: User not authenticated, showing fallback while redirecting');
    return fallback;
  }

  console.log('ProtectedRoute: User authenticated, rendering children');
  return <>{children}</>;
};

export { ProtectedRoute };