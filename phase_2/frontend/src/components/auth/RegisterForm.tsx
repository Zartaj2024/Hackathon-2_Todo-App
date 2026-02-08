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

const registerSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number')
    .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

const RegisterForm = () => {
  const { register: authRegister, isLoading } = useAuth(); // Updated hook - using register instead of signUp, renamed to avoid conflict
  const authError = null; // Updated - using register hook doesn't have error property

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const [submitError, setSubmitError] = React.useState<string | null>(null);

  const onSubmit = async (data: RegisterFormData) => {
    setSubmitError(null); // Clear previous error

    try {
      await authRegister(data.email, data.password, data.name);
      // If registration succeeds, the user will be redirected by the context
    } catch (error: any) {
      console.error('Registration failed:', error);
      const errorMessage = error.message || 'Registration failed. Please try again.';
      setSubmitError(errorMessage);

      // Set field-specific errors if needed
      if (errorMessage.includes('email') && errorMessage.toLowerCase().includes('registered')) {
        setError('email', { message: 'This email is already registered' });
      }
    }
  };

  // Combine auth error and submit error for display
  const displayError = authError || submitError;

  return (
    <Card title="Create a new account" className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <Input
            {...register('name')}
            label="Full Name"
            type="text"
            placeholder="John Doe"
            error={errors.name?.message}
          />
        </div>

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
          <p className="mt-1 text-xs text-gray-500">
            Password must be at least 8 characters with uppercase, lowercase, number, and special character
          </p>
        </div>

        <div>
          <Input
            {...register('confirmPassword')}
            label="Confirm Password"
            type="password"
            placeholder="••••••••"
            error={errors.confirmPassword?.message}
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
            Sign up
          </Button>
        </div>
      </form>

      <div className="mt-4 text-center text-sm text-gray-600">
        <p>
          Already have an account?{' '}
          <Link href={"/login" as any} className="font-medium text-blue-600 hover:text-blue-500">
            Sign in
          </Link>
        </p>
      </div>
    </Card>
  );
};

export { RegisterForm };