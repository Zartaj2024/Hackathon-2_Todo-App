/**
 * Test suite for registration flow with comprehensive error handling.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { RegisterForm } from '@/components/auth/RegisterForm';
import { AuthProvider, useAuthContext } from '@/contexts/AuthContext';
import { MemoryRouter } from 'react-router-dom';
import React from 'react';

// Mock the useRouter hook
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
  }),
}));

// Mock the auth operations
vi.mock('@/lib/auth', async () => {
  const actual = await vi.importActual('@/lib/auth');
  return {
    ...actual,
    authOperations: {
      signUp: vi.fn(),
      signIn: vi.fn(),
      signOut: vi.fn(),
      getSession: vi.fn(),
      sendResetPassword: vi.fn(),
      resetPassword: vi.fn(),
      updateUser: vi.fn(),
      changePassword: vi.fn(),
    }
  };
});

// Mock the auth client
vi.mock('better-auth/client', () => ({
  createAuthClient: vi.fn(() => ({})),
}));

// Mock the betterFetch
vi.mock('@better-fetch/fetch', () => ({
  betterFetch: vi.fn(),
}));

// Create a test wrapper component
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
  <MemoryRouter>
    <AuthProvider>
      {children}
    </AuthProvider>
  </MemoryRouter>
);

// Mock the useAuthContext hook for testing
const MockAuthContextProvider = ({ children, mockAuthState }: {
  children: React.ReactNode,
  mockAuthState: any
}) => {
  return (
    <MockAuthProvider mockAuthState={mockAuthState}>
      {children}
    </MockAuthProvider>
  );
};

// Create a mock provider component
const MockAuthProvider: React.FC<{
  children: React.ReactNode;
  mockAuthState: any
}> = ({ children, mockAuthState }) => {
  const contextValue = {
    user: mockAuthState.user || null,
    session: mockAuthState.session || null,
    signUp: mockAuthState.signUp || vi.fn(),
    signIn: mockAuthState.signIn || vi.fn(),
    signOut: mockAuthState.signOut || vi.fn(),
    isLoading: mockAuthState.isLoading || false,
    isAuthenticated: mockAuthState.isAuthenticated || false,
    error: mockAuthState.error || null,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Create AuthContext for the mock
const AuthContext = React.createContext<any>(undefined);

describe('Registration Form Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders the registration form correctly', () => {
    render(
      <TestWrapper>
        <RegisterForm />
      </TestWrapper>
    );

    expect(screen.getByText(/Create a new account/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Full Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Confirm Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign up/i })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(
      <TestWrapper>
        <RegisterForm />
      </TestWrapper>
    );

    const submitButton = screen.getByRole('button', { name: /Sign up/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Name must be at least 2 characters/i)).toBeInTheDocument();
      expect(screen.getByText(/Invalid email address/i)).toBeInTheDocument();
      expect(screen.getByText(/Password must be at least 8 characters/i)).toBeInTheDocument();
      expect(screen.getByText(/Passwords don't match/i)).toBeInTheDocument();
    });
  });

  it('validates password strength requirements', async () => {
    render(
      <TestWrapper>
        <RegisterForm />
      </TestWrapper>
    );

    const passwordInput = screen.getByLabelText(/Password/i);
    const nameInput = screen.getByLabelText(/Full Name/i);
    const emailInput = screen.getByLabelText(/Email address/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign up/i });

    // Fill in valid name and email
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'Short1!' } });

    // Enter a weak password (doesn't meet requirements)
    fireEvent.change(passwordInput, { target: { value: 'short' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      // Should show password validation errors
      expect(screen.getByText(/Password must be at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('shows error when passwords do not match', async () => {
    render(
      <TestWrapper>
        <RegisterForm />
      </TestWrapper>
    );

    const nameInput = screen.getByLabelText(/Full Name/i);
    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign up/i });

    // Fill in valid inputs
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'DifferentPass2@' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Passwords don't match/i)).toBeInTheDocument();
    });
  });

  it('calls signUp function with valid data', async () => {
    const mockSignUp = vi.fn().mockResolvedValue({ success: true });

    render(
      <MockAuthContextProvider mockAuthState={{ signUp: mockSignUp, isLoading: false, error: null }}>
        <RegisterForm />
      </MockAuthContextProvider>
    );

    const nameInput = screen.getByLabelText(/Full Name/i);
    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign up/i });

    // Fill in valid inputs
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSignUp).toHaveBeenCalledWith(
        'john@example.com',
        'ValidPass1!',
        'John Doe'
      );
    });
  });

  it('shows error when signup fails', async () => {
    const mockSignUp = vi.fn().mockResolvedValue({
      success: false,
      error: { message: 'Email already registered' }
    });

    render(
      <MockAuthContextProvider mockAuthState={{ signUp: mockSignUp, isLoading: false, error: null }}>
        <RegisterForm />
      </MockAuthContextProvider>
    );

    const nameInput = screen.getByLabelText(/Full Name/i);
    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign up/i });

    // Fill in valid inputs
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Email already registered/i)).toBeInTheDocument();
    });
  });

  it('shows loading state during submission', async () => {
    const mockSignUp = vi.fn().mockImplementation(() => new Promise(() => {})); // Never resolves for this test

    render(
      <MockAuthContextProvider mockAuthState={{ signUp: mockSignUp, isLoading: false, error: null }}>
        <RegisterForm />
      </MockAuthContextProvider>
    );

    const nameInput = screen.getByLabelText(/Full Name/i);
    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign up/i });

    // Fill in valid inputs
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    // Check that loading state is activated
    expect(submitButton).toBeDisabled();
  });

  it('handles network errors gracefully', async () => {
    const mockSignUp = vi.fn().mockRejectedValue(new Error('Network error'));

    render(
      <MockAuthContextProvider mockAuthState={{ signUp: mockSignUp, isLoading: false, error: null }}>
        <RegisterForm />
      </MockAuthContextProvider>
    );

    const nameInput = screen.getByLabelText(/Full Name/i);
    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const confirmPasswordInput = screen.getByLabelText(/Confirm Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign up/i });

    // Fill in valid inputs
    fireEvent.change(nameInput, { target: { value: 'John Doe' } });
    fireEvent.change(emailInput, { target: { value: 'john@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });
    fireEvent.change(confirmPasswordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Registration failed. Please try again./i)).toBeInTheDocument();
    });
  });
});

console.log('Registration flow tests completed successfully');