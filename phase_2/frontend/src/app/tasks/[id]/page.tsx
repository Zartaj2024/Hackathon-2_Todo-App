'use client';

import { useParams, useRouter } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { taskService } from '@/lib/api/tasks';

export default function TaskDetailPage() {
  const { id } = useParams();
  const taskId = Array.isArray(id) ? parseInt(id[0] ?? '0', 10) : parseInt(id ?? '0', 10);
  const router = useRouter();

  const { data: task, error, isLoading } = taskService.useTask(taskId);

  if (isLoading) {
    return (
      <ProtectedRoute>
        <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <Card>
            <div className="py-12 flex flex-col items-center justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-600">Loading task...</p>
            </div>
          </Card>
        </div>
      </ProtectedRoute>
    );
  }

  if (error || !task) {
    return (
      <ProtectedRoute>
        <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <Card>
            <div className="py-12 flex flex-col items-center justify-center">
              <div className="text-red-500 text-xl font-medium">
                {error ? 'Error loading task' : 'Task not found'}
              </div>
              <p className="mt-2 text-gray-600">
                {error?.message || 'The requested task could not be found.'}
              </p>
            </div>
          </Card>
        </div>
      </ProtectedRoute>
    );
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Task Details</h1>
          <Button variant="outline" onClick={() => router.push(`/tasks/${taskId}/edit`)}>
            Edit Task
          </Button>
        </div>

        <Card>
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">{task.title}</h2>
              <div className="mt-2 flex items-center">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  task.completed
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {task.completed ? 'Completed' : 'Pending'}
                </span>
                {task.priority && (
                  <span className="ml-3 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                    Priority: {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                  </span>
                )}
                {task.category && (
                  <span className="ml-3 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                    {task.category}
                  </span>
                )}
              </div>
            </div>

            {task.description && (
              <div>
                <h3 className="text-sm font-medium text-gray-700">Description</h3>
                <p className="mt-1 text-gray-900">{task.description}</p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-sm font-medium text-gray-700">Created</h3>
                <p className="mt-1 text-gray-900">{formatDate(task.createdAt)}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-700">Updated</h3>
                <p className="mt-1 text-gray-900">{formatDate(task.updatedAt)}</p>
              </div>
              {task.dueDate && (
                <>
                  <div>
                    <h3 className="text-sm font-medium text-gray-700">Due Date</h3>
                    <p className="mt-1 text-gray-900">{formatDate(task.dueDate)}</p>
                  </div>
                </>
              )}
            </div>

            <div className="flex space-x-4 pt-4">
              <Button
                variant={task.completed ? 'secondary' : 'primary'}
                onClick={() => taskService.toggleComplete(task.id)}
              >
                {task.completed ? 'Mark as Incomplete' : 'Mark as Complete'}
              </Button>
              <Button
                variant="danger"
                onClick={() => {
                  if (confirm('Are you sure you want to delete this task?')) {
                    taskService.delete(task.id);
                  }
                }}
              >
                Delete Task
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </ProtectedRoute>
  );
}