'use client';

import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { TaskForm } from '@/components/tasks/TaskForm';
import { taskService } from '@/lib/api/tasks';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth/context';

export default function NewTaskPage() {
  const router = useRouter();
  const { user } = useAuth();

  const handleCreateTask = async (formData: any) => {
    try {
      // Add user_id to the form data as required by the backend API
      const taskData = {
        ...formData,
        user_id: user?.id,  // Include the authenticated user's ID
      };

      await taskService.create(taskData);
      router.push('/tasks');
      router.refresh(); // Refresh to update the task list
    } catch (error) {
      console.error('Failed to create task:', error);
      // In a real app, you would show an error message to the user
    }
  };

  const handleCancel = () => {
    router.push('/tasks');
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={handleCancel}
          submitLabel="Create Task"
        />
      </div>
    </ProtectedRoute>
  );
}