'use client';

import { useParams, useRouter } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { TaskForm } from '@/components/tasks/TaskForm';
import { taskService } from '@/lib/api/tasks';
import { useAuth } from '@/lib/auth/context';

export default function EditTaskPage() {
  const { id } = useParams();
  const router = useRouter();
  const { user } = useAuth();

  const taskId = Array.isArray(id) ? parseInt(id[0] ?? '0', 10) : parseInt(id ?? '0', 10);

  const { data: task, error, isLoading } = taskService.useTask(taskId);

  const handleUpdateTask = async (formData: any) => {
    try {
      // Include user_id in the form data as required by the backend API
      const taskData = {
        ...formData,
        user_id: user?.id,  // Include the authenticated user's ID
      };

      await taskService.update(taskId, taskData, user?.id);
      router.push(`/tasks/${taskId}`);
      router.refresh(); // Refresh to update the task detail view
    } catch (error) {
      console.error('Failed to update task:', error);
      // In a real app, you would show an error message to the user
    }
  };

  const handleCancel = () => {
    router.push(`/tasks/${taskId}`);
  };

  if (isLoading) {
    return (
      <ProtectedRoute>
        <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading task...</p>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  if (error || !task) {
    return (
      <ProtectedRoute>
        <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="text-red-500 text-xl font-medium">
              {error ? 'Error loading task' : 'Task not found'}
            </div>
            <p className="mt-2 text-gray-600">
              {error?.message || 'The requested task could not be found.'}
            </p>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  // Prepare initial data for the form
  const initialData = {
    title: task.title,
    description: task.description || '',
    priority: task.priority || 'medium',
    dueDate: task.dueDate || '',
    category: task.category || '',
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <TaskForm
          initialData={initialData}
          onSubmit={handleUpdateTask}
          onCancel={handleCancel}
          submitLabel="Update Task"
        />
      </div>
    </ProtectedRoute>
  );
}