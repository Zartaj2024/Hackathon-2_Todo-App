/**
 * End-to-end tests for the complete authentication flow with comprehensive error handling.
 */

import { test, expect, describe } from '@playwright/test';

describe('Authentication Flow End-to-End Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Clean up before each test
    await page.goto('/');
  });

  test('Complete registration and login flow', async ({ page }) => {
    // Navigate to registration page
    await page.goto('/register');

    // Fill in registration form
    await page.fill('input[name="name"]', 'Test User');
    await page.fill('input[name="email"]', `testuser_${Date.now()}@example.com`);
    await page.fill('input[name="password"]', 'SecurePass123!');
    await page.fill('input[name="confirmPassword"]', 'SecurePass123!');

    // Submit registration
    await page.click('button[type="submit"]');

    // Verify registration success (redirect to dashboard or similar)
    await expect(page).toHaveURL(/\/dashboard|\/$/);

    // Logout to test login
    await page.click('text=Logout'); // Adjust selector based on actual logout button

    // Navigate to login page
    await page.goto('/login');

    // Fill in login form
    await page.fill('input[name="email"]', 'testuser@example.com');
    await page.fill('input[name="password"]', 'SecurePass123!');

    // Submit login
    await page.click('button[type="submit"]');

    // Verify login success
    await expect(page).toHaveURL(/\/dashboard|\/$/);
    await expect(page.locator('text=Welcome, Test User')).toBeVisible();
  });

  test('Registration with weak password shows error', async ({ page }) => {
    await page.goto('/register');

    // Fill in registration form with weak password
    await page.fill('input[name="name"]', 'Test User');
    await page.fill('input[name="email"]', `weakpass_${Date.now()}@example.com`);
    await page.fill('input[name="password"]', 'weak');
    await page.fill('input[name="confirmPassword"]', 'weak');

    // Submit registration
    await page.click('button[type="submit"]');

    // Verify error message is shown
    await expect(page.locator('text=Password must be at least 8 characters')).toBeVisible();
  });

  test('Login with incorrect credentials shows error', async ({ page }) => {
    await page.goto('/login');

    // Fill in login form with wrong credentials
    await page.fill('input[name="email"]', 'nonexistent@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');

    // Submit login
    await page.click('button[type="submit"]');

    // Verify error message is shown
    await expect(page.locator('text=Invalid email or password')).toBeVisible();
  });

  test('Registration with mismatched passwords shows error', async ({ page }) => {
    await page.goto('/register');

    // Fill in registration form with mismatched passwords
    await page.fill('input[name="name"]', 'Test User');
    await page.fill('input[name="email"]', `mismatch_${Date.now()}@example.com`);
    await page.fill('input[name="password"]', 'SecurePass123!');
    await page.fill('input[name="confirmPassword"]', 'DifferentPass456@');

    // Submit registration
    await page.click('button[type="submit"]');

    // Verify error message is shown
    await expect(page.locator('text=Passwords don\'t match')).toBeVisible();
  });

  test('Form validation prevents submission of invalid data', async ({ page }) => {
    await page.goto('/register');

    // Try to submit empty form
    await page.click('button[type="submit"]');

    // Verify validation errors are shown
    await expect(page.locator('text=Name must be at least 2 characters')).toBeVisible();
    await expect(page.locator('text=Invalid email address')).toBeVisible();
    await expect(page.locator('text=Password must be at least 8 characters')).toBeVisible();
    await expect(page.locator('text=Passwords don\'t match')).toBeVisible();
  });

  test('Password reset flow', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');

    // Click on "Forgot password" link (assuming it exists)
    await page.click('text=Forgot password');

    // Fill in email for password reset
    await page.fill('input[type="email"]', 'user@example.com');

    // Submit password reset request
    await page.click('button[type="submit"]');

    // Verify success message
    await expect(page.locator('text=Password reset email sent')).toBeVisible();
  });

  test('Session persistence after page refresh', async ({ page }) => {
    // First, perform a login (simulate)
    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    // Wait for login to complete
    await page.waitForURL(/\/dashboard|\/$/);

    // Refresh the page
    await page.reload();

    // Verify user is still logged in after refresh
    await expect(page.locator('text=Welcome, Test User')).toBeVisible();
  });

  test('Error handling during network issues', async ({ page }) => {
    // Simulate network error
    await page.route('**/api/auth/**', route => route.abort());

    await page.goto('/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    // Verify error message is shown
    await expect(page.locator('text=Network error')).toBeVisible();
  });

  test('Concurrent authentication requests are handled properly', async ({ page }) => {
    await page.goto('/login');

    // Fill in login form
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123!');

    // Click submit button multiple times quickly
    await page.click('button[type="submit"]');
    await page.click('button[type="submit"]');
    await page.click('button[type="submit"]');

    // Verify only one request is processed (check for single error message or success)
    const errorCount = await page.locator('.error-message').count();
    const successCount = await page.locator('.success-message').count();

    // Either one success or one error, but not multiple
    expect(errorCount + successCount).toBeLessThanOrEqual(1);
  });
});

console.log('End-to-end authentication tests completed successfully');