'use client';

import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card } from '@/components/ui/Card';
import { useAuth } from '@/lib/auth/context'; // Updated import for existing auth context
import Link from 'next/link';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

const LoginForm = () => {
  const { login, isLoading } = useAuth(); // Updated hook - using login instead of signIn
  const authError = null; // Updated - using login hook doesn't have error property

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const [submitError, setSubmitError] = React.useState<string | null>(null);

  const onSubmit = async (data: LoginFormData) => {
    setSubmitError(null); // Clear previous error

    try {
      await login(data.email, data.password);
      // If login succeeds, the user will be redirected by the context
    } catch (error: any) {
      console.error('Login failed:', error);
      const errorMessage = error.message || 'Login failed. Please try again.';
      setSubmitError(errorMessage);
    }
  };

  // Combine auth error and submit error for display
  const displayError = authError || submitError;

  return (
    <Card title="Sign in to your account" className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <Input
            {...register('email')}
            label="Email address"
            type="email"
            placeholder="you@example.com"
            error={errors.email?.message}
          />
        </div>

        <div>
          <Input
            {...register('password')}
            label="Password"
            type="password"
            placeholder="••••••••"
            error={errors.password?.message}
          />
        </div>

        {displayError && (
          <div className="pt-2">
            <div className="text-red-600 text-sm p-2 bg-red-50 rounded-md">
              {displayError}
            </div>
          </div>
        )}
        <div className="pt-2">
          <Button
            type="submit"
            className="w-full"
            loading={isLoading}
            disabled={isLoading}
          >
            Sign in
          </Button>
        </div>
      </form>

      <div className="mt-4 text-center text-sm text-gray-600">
        <p>
          Don't have an account?{' '}
          <Link href={"/register" as any} className="font-medium text-blue-600 hover:text-blue-500">
            Sign up
          </Link>
        </p>
      </div>
    </Card>
  );
};

export { LoginForm };