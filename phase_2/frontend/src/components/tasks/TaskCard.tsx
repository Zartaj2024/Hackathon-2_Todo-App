import React from 'react';
import { Task } from '@/lib/types/task';
import { Button } from '@/components/ui/Button';
import { formatDate } from '@/utils/date';

interface TaskCardProps {
  task: Task;
  onToggleComplete?: (id: number) => void;
  onDelete?: (id: number) => void;
  onEdit?: (task: Task) => void;
}

const getPriorityColor = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'border-l-danger-500 bg-danger-50 dark:bg-danger-900/20';
    case 'medium':
      return 'border-l-warning-500 bg-warning-50 dark:bg-warning-900/20';
    case 'low':
      return 'border-l-success-500 bg-success-50 dark:bg-success-900/20';
    default:
      return 'border-l-gray-300 bg-gray-50 dark:bg-gray-800/50';
  }
};

const getPriorityDotColor = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'bg-danger-500';
    case 'medium':
      return 'bg-warning-500';
    case 'low':
      return 'bg-success-500';
    default:
      return 'bg-gray-300';
  }
};

const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onToggleComplete,
  onDelete,
  onEdit,
}) => {
  const handleToggleComplete = () => {
    onToggleComplete?.(task.id);
  };

  const handleDelete = () => {
    onDelete?.(task.id);
  };

  const handleEdit = () => {
    onEdit?.(task);
  };

  return (
    <div className={`border-l-4 border border-gray-200 rounded-lg p-4 hover:shadow-md transition-all duration-200 ${getPriorityColor(task.priority || 'medium')} dark:border-gray-700`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1 min-w-0">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleComplete}
            className="mt-1 h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2">
              <h3
                className={`text-lg font-medium ${
                  task.completed ? 'text-gray-500 line-through' : 'text-gray-900 dark:text-white'
                }`}
              >
                {task.title}
              </h3>
              <span className={`w-2 h-2 rounded-full ${getPriorityDotColor(task.priority || 'medium')}`} title={`Priority: ${task.priority || 'medium'}`} />
            </div>
            {task.description && (
              <p className="mt-1 text-gray-600 dark:text-gray-300 truncate">{task.description}</p>
            )}
            <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
              <span className="text-gray-500 dark:text-gray-400">Created: {formatDate(task.createdAt)}</span>
              {task.dueDate && (
                <span className="text-gray-500 dark:text-gray-400">Due: {formatDate(task.dueDate)}</span>
              )}
              {task.completed && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-success-100 text-success-800 dark:bg-success-900/30 dark:text-success-300">
                  Completed
                </span>
              )}
            </div>
            {task.tags && task.tags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-2">
                {task.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900/30 dark:text-primary-300"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="flex space-x-2 ml-4">
          <Button
            variant="outline"
            size="sm"
            onClick={handleEdit}
            disabled={!onEdit}
          >
            Edit
          </Button>
          <Button
            variant="danger"
            size="sm"
            onClick={handleDelete}
            disabled={!onDelete}
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
};

export { TaskCard };