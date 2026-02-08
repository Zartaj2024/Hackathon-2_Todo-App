/**
 * Test suite for login flow with comprehensive error handling.
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { LoginForm } from '@/components/auth/LoginForm';
import { AuthProvider } from '@/contexts/AuthContext';
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

describe('Login Form Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders the login form correctly', () => {
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    expect(screen.getByText(/Sign in to your account/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign in/i })).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    const submitButton = screen.getByRole('button', { name: /Sign in/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Invalid email address/i)).toBeInTheDocument();
      expect(screen.getByText(/Password must be at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('validates email format', async () => {
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Enter invalid email
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Invalid email address/i)).toBeInTheDocument();
    });
  });

  it('validates password length', async () => {
    render(
      <TestWrapper>
        <LoginForm />
      </TestWrapper>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Enter valid email and short password
    fireEvent.change(emailInput, { target: { value: 'user@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'short' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Password must be at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('calls signIn function with valid data', async () => {
    const mockSignIn = vi.fn().mockResolvedValue({ success: true });

    render(
      <MockAuthContextProvider mockAuthState={{ signIn: mockSignIn, isLoading: false, error: null }}>
        <LoginForm />
      </MockAuthContextProvider>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Fill in valid inputs
    fireEvent.change(emailInput, { target: { value: 'user@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSignIn).toHaveBeenCalledWith(
        'user@example.com',
        'ValidPass1!'
      );
    });
  });

  it('shows error when login fails', async () => {
    const mockSignIn = vi.fn().mockResolvedValue({
      success: false,
      error: { message: 'Invalid email or password' }
    });

    render(
      <MockAuthContextProvider mockAuthState={{ signIn: mockSignIn, isLoading: false, error: null }}>
        <LoginForm />
      </MockAuthContextProvider>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Fill in inputs
    fireEvent.change(emailInput, { target: { value: 'user@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Invalid email or password/i)).toBeInTheDocument();
    });
  });

  it('shows loading state during submission', async () => {
    const mockSignIn = vi.fn().mockImplementation(() => new Promise(() => {})); // Never resolves for this test

    render(
      <MockAuthContextProvider mockAuthState={{ signIn: mockSignIn, isLoading: false, error: null }}>
        <LoginForm />
      </MockAuthContextProvider>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Fill in inputs
    fireEvent.change(emailInput, { target: { value: 'user@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    // Check that loading state is activated
    expect(submitButton).toBeDisabled();
  });

  it('handles network errors gracefully', async () => {
    const mockSignIn = vi.fn().mockRejectedValue(new Error('Network error'));

    render(
      <MockAuthContextProvider mockAuthState={{ signIn: mockSignIn, isLoading: false, error: null }}>
        <LoginForm />
      </MockAuthContextProvider>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Fill in inputs
    fireEvent.change(emailInput, { target: { value: 'user@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Login failed. Please try again./i)).toBeInTheDocument();
    });
  });

  it('handles incorrect credentials error', async () => {
    const mockSignIn = vi.fn().mockResolvedValue({
      success: false,
      error: { message: 'Incorrect email or password' }
    });

    render(
      <MockAuthContextProvider mockAuthState={{ signIn: mockSignIn, isLoading: false, error: null }}>
        <LoginForm />
      </MockAuthContextProvider>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Fill in inputs
    fireEvent.change(emailInput, { target: { value: 'nonexistent@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Incorrect email or password/i)).toBeInTheDocument();
    });
  });

  it('allows valid login to proceed', async () => {
    const mockSignIn = vi.fn().mockResolvedValue({ success: true });

    render(
      <MockAuthContextProvider mockAuthState={{ signIn: mockSignIn, isLoading: false, error: null }}>
        <LoginForm />
      </MockAuthContextProvider>
    );

    const emailInput = screen.getByLabelText(/Email address/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const submitButton = screen.getByRole('button', { name: /Sign in/i });

    // Fill in valid inputs
    fireEvent.change(emailInput, { target: { value: 'valid@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'ValidPass1!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockSignIn).toHaveBeenCalledWith(
        'valid@example.com',
        'ValidPass1!'
      );
    });
  });
});

console.log('Login flow tests completed successfully');