'use client';

import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { Card } from '@/components/ui/Card';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400 font-medium">
            Welcome to your todo application. Manage your tasks efficiently.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card title="Quick Stats" className="glow-hover">
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400 font-medium">Total Tasks</span>
                <span className="font-bold text-primary-600 dark:text-primary-400">0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400 font-medium">Completed</span>
                <span className="font-bold text-success-600 dark:text-success-400">0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400 font-medium">Pending</span>
                <span className="font-bold text-warning-600 dark:text-warning-400">0</span>
              </div>
            </div>
          </Card>

          <Card title="Quick Actions" className="glow-hover">
            <div className="space-y-3">
              <Link href={"/tasks" as any}>
                <Button variant="primary" fullWidth className="h-11">
                  View All Tasks
                </Button>
              </Link>
              <Link href={"/tasks/new" as any}>
                <Button variant="outline" fullWidth className="h-11">
                  Create New Task
                </Button>
              </Link>
              <Link href={"/chat" as any}>
                <Button variant="premium" fullWidth className="h-11">
                  Open AI Assistant
                </Button>
              </Link>
            </div>
          </Card>

          <Card title="Upcoming" className="glow-hover">
            <p className="text-gray-500 dark:text-gray-500 text-center py-4 italic">
              No upcoming tasks scheduled
            </p>
          </Card>
        </div>

        <div className="mt-8">
          <Card className="glass-card">
            <div className="text-center py-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Need Help Managing Tasks?
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-6 font-medium max-w-xl mx-auto">
                Our AI assistant can help you create and manage tasks. Just ask to prioritize, summarize, or breakdown your goals.
              </p>
              <Link href={"/chat" as any}>
                <Button variant="premium" size="lg" className="px-8 shadow-glow">
                  Talk to AI Assistant
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </ProtectedRoute>
  );
}