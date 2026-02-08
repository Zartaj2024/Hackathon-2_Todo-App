import React from 'react';
import { Task } from '@/lib/types/task';
import { TaskCard } from '@/components/tasks/TaskCard';
import { Card } from '@/components/ui/Card';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete?: (id: number) => void;
  onDelete?: (id: number) => void;
  onEdit?: (task: Task) => void;
  loading?: boolean;
  error?: string;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleComplete,
  onDelete,
  onEdit,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <Card className="w-full">
        <div className="py-12 flex flex-col items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading tasks...</p>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full">
        <div className="py-12 flex flex-col items-center justify-center">
          <div className="text-red-500 text-xl font-medium">Error loading tasks</div>
          <p className="mt-2 text-gray-600">{error}</p>
        </div>
      </Card>
    );
  }

  if (!tasks || tasks.length === 0) {
    return (
      <Card className="w-full">
        <div className="py-12 text-center">
          <p className="text-gray-600">No tasks found. Create your first task!</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
};

export { TaskList };