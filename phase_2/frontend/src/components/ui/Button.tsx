import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'ghost' | 'link' | 'outline' | 'premium';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  loading?: boolean;
  icon?: React.ReactNode;
  fullWidth?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    children,
    variant = 'primary',
    size = 'md',
    loading,
    icon,
    fullWidth = false,
    className = '',
    disabled,
    ...props
  }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center font-bold rounded-xl transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transform active:scale-[0.96] select-none';

    const variantClasses = {
      primary: 'bg-primary-600 text-white shadow-lg shadow-primary-500/20 hover:bg-primary-700 hover:shadow-primary-500/40 focus:ring-primary-500',
      secondary: 'bg-white text-gray-700 border border-gray-200 shadow-sm hover:bg-gray-50 hover:text-gray-900 focus:ring-gray-200 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-700 dark:hover:bg-gray-700',
      success: 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/20 hover:bg-emerald-700 hover:shadow-emerald-500/40 focus:ring-emerald-500',
      danger: 'bg-rose-600 text-white shadow-lg shadow-rose-500/20 hover:bg-rose-700 hover:shadow-rose-500/40 focus:ring-rose-500',
      warning: 'bg-amber-500 text-white shadow-lg shadow-amber-500/20 hover:bg-amber-600 hover:shadow-amber-500/40 focus:ring-amber-500',
      ghost: 'bg-transparent text-gray-600 hover:bg-gray-100 hover:text-gray-900 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-100',
      link: 'bg-transparent text-primary-600 hover:text-primary-700 hover:underline focus:ring-primary-500 p-0 h-auto font-normal',
      outline: 'bg-transparent border-2 border-primary-600 text-primary-600 hover:bg-primary-50 hover:shadow-primary-600/10 focus:ring-primary-500 dark:border-primary-500 dark:text-primary-500 dark:hover:bg-primary-900/20',
      premium: 'premium-gradient text-white shadow-lg shadow-primary-500/25 hover:shadow-glow hover:scale-[1.02] active:scale-[0.98] border border-white/10',
    };

    const sizeClasses = {
      xs: 'text-xs px-3 py-1.5',
      sm: 'text-sm px-4 py-2',
      md: 'text-sm px-6 py-2.5',
      lg: 'text-base px-8 py-3.5',
      xl: 'text-lg px-10 py-4.5',
    };

    const widthClass = fullWidth ? 'w-full' : '';

    const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${widthClass} ${className}`;

    return (
      <button
        ref={ref}
        className={classes}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg
            className="animate-spin -ml-1 mr-3 h-4 w-4 text-current"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        )}
        {icon && !loading && <span className="mr-2 scale-110">{icon}</span>}
        <span className="relative z-10">{children}</span>
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button };