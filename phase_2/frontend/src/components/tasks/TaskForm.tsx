'use client';

import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';

const taskSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  description: z.string().optional(),
  priority: z.enum(['low', 'medium', 'high']).optional(),
  dueDate: z.string().optional(),
  category: z.string().optional(),
  tags: z.string().optional(),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface TaskFormProps {
  initialData?: TaskFormData;
  onSubmit: (data: TaskFormData) => void;
  onCancel?: () => void;
  submitLabel?: string;
  loading?: boolean;
}

const TaskForm: React.FC<TaskFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = 'Create Task',
  loading = false,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: initialData || {
      title: '',
      description: '',
      priority: 'medium',
      dueDate: '',
      category: '',
      tags: '',
    },
  });

  const currentPriority = watch('priority') || 'medium';

  const handlePriorityChange = (priority: 'low' | 'medium' | 'high') => {
    setValue('priority', priority);
  };

  return (
    <Card title={initialData ? 'Edit Task' : 'Create New Task'} variant="elevated">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div>
          <Input
            {...register('title')}
            label="Task Title"
            type="text"
            placeholder="Enter task title"
            error={errors.title?.message}
            inputSize="lg"
            fullWidth
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1 dark:text-gray-300">
            Description
          </label>
          <textarea
            id="description"
            {...register('description')}
            placeholder="Enter task description"
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:focus:ring-primary-600 dark:focus:border-primary-600"
          />
          {errors.description && (
            <p className="mt-1 text-sm text-danger-600 dark:text-danger-500">{errors.description.message}</p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1 dark:text-gray-300">
              Priority
            </label>
            <div className="grid grid-cols-3 gap-2">
              {(['low', 'medium', 'high'] as const).map((priority) => (
                <button
                  key={priority}
                  type="button"
                  className={`py-3 px-3 rounded-lg text-sm font-medium transition-colors duration-200 ${currentPriority === priority
                    ? priority === 'high'
                      ? 'bg-danger-600 text-white ring-2 ring-danger-500 ring-offset-2'
                      : priority === 'medium'
                        ? 'bg-warning-500 text-white ring-2 ring-warning-400 ring-offset-2'
                        : 'bg-success-600 text-white ring-2 ring-success-500 ring-offset-2'
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600'
                    }`}
                  onClick={() => handlePriorityChange(priority)}
                  aria-pressed={currentPriority === priority}
                >
                  {priority.charAt(0).toUpperCase() + priority.slice(1)}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <Input
                {...register('category')}
                label="Category"
                type="text"
                placeholder="Work, Personal, Shopping, etc."
                error={errors.category?.message}
                inputSize="md"
              />
            </div>

            <div>
              <Input
                {...register('tags')}
                label="Tags (comma separated)"
                type="text"
                placeholder="project, urgent, meeting, etc."
                error={errors.tags?.message}
                inputSize="md"
              />
            </div>
          </div>
        </div>

        <div>
          <Input
            {...register('dueDate')}
            label="Due Date"
            type="date"
            error={errors.dueDate?.message}
            inputSize="md"
          />
        </div>

        <div className="flex flex-col sm:flex-row sm:space-x-3 sm:space-y-0 space-y-3 pt-4">
          <Button
            type="submit"
            loading={loading}
            disabled={loading}
            size="lg"
            className="flex-1"
          >
            {submitLabel}
          </Button>
          {onCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={loading}
              size="lg"
              className="flex-1"
            >
              Cancel
            </Button>
          )}
        </div>
      </form>
    </Card>
  );
};

export { TaskForm };