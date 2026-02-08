'use client';

import { ProtectedRoute } from '@/components/auth/ProtectedRoute';
import { TaskList } from '@/components/tasks/TaskList';
import { Button } from '@/components/ui/Button';
import { taskService } from '@/lib/api/tasks';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function TasksPage() {
  const { data: tasks, error, isLoading } = taskService.useTasks();
  const router = useRouter();

  const handleEditTask = (task: any) => {
    router.push(`/tasks/${task.id}/edit`);
  };

  return (
    <ProtectedRoute>
      <div className="container mx-auto py-6 sm:py-8 px-4">
        <div className="mb-6 sm:mb-8 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">My Tasks</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              {tasks?.length ?? 0} task{tasks?.length !== 1 ? 's' : ''} total
            </p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
            <Link href={"/chat" as any} className="w-full sm:w-auto">
              <Button variant="secondary" fullWidth>
                AI Assistant
              </Button>
            </Link>
            <Link href={"/tasks/new" as any} className="w-full sm:w-auto">
              <Button variant="primary" fullWidth>
                Create New Task
              </Button>
            </Link>
          </div>
        </div>

        <TaskList
          tasks={tasks || []}
          loading={isLoading}
          error={error?.message}
          onToggleComplete={(id) => taskService.toggleComplete(id)}
          onDelete={(id) => taskService.delete(id)}
          onEdit={handleEditTask}
        />
      </div>
    </ProtectedRoute>
  );
}