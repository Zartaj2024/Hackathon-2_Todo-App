import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  variant?: 'default' | 'success' | 'error';
  startIcon?: React.ReactNode;
  endIcon?: React.ReactNode;
  inputSize?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({
    label,
    error,
    helperText,
    variant = 'default',
    startIcon,
    endIcon,
    inputSize = 'md',
    fullWidth = false,
    className = '',
    ...props
  }, ref) => {
    const hasError = !!error;

    const sizeClasses = {
      sm: 'px-3 py-2 text-sm',
      md: 'px-4 py-3 text-sm',
      lg: 'px-5 py-4 text-base font-medium',
    };

    const widthClass = fullWidth ? 'w-full' : 'w-full';

    const paddingLeft = startIcon ? (inputSize === 'sm' ? 'pl-9' : inputSize === 'lg' ? 'pl-11' : 'pl-10') : '';
    const paddingRight = endIcon ? (inputSize === 'sm' ? 'pr-9' : inputSize === 'lg' ? 'pr-11' : 'pr-10') : '';

    return (
      <div className={`${widthClass} group`}>
        {label && (
          <label className="block text-sm font-bold text-gray-700 mb-2 dark:text-gray-300 group-focus-within:text-primary-500 transition-colors duration-200">
            {label}
          </label>
        )}
        <div className="relative">
          {startIcon && (
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400 group-focus-within:text-primary-500 transition-colors duration-200">
              {startIcon}
            </div>
          )}

          <input
            ref={ref}
            className={`
              block w-full rounded-xl transition-all duration-300 
              disabled:opacity-60 disabled:bg-gray-100 disabled:cursor-not-allowed
              focus:outline-none focus:ring-4 focus:ring-primary-500/10
              placeholder-gray-400 dark:placeholder-gray-600 font-medium
              ${sizeClasses[inputSize]} 
              ${paddingLeft} ${paddingRight}
              ${hasError
                ? 'border-2 border-rose-500 bg-rose-50 text-rose-900 focus:border-rose-600 dark:bg-rose-900/10 dark:text-rose-100'
                : 'border border-gray-200 bg-white shadow-sm focus:border-primary-500 dark:border-gray-800 dark:bg-slate-900/50 dark:text-white dark:backdrop-blur-sm'
              } 
              ${className}
            `}
            {...props}
          />

          {endIcon && (
            <div className="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none text-gray-400 group-focus-within:text-primary-500 transition-colors duration-200">
              {endIcon}
            </div>
          )}
        </div>

        {error && (
          <p className="mt-2 text-sm text-rose-600 dark:text-rose-400 font-bold flex items-center gap-1 animate-in fade-in slide-in-from-top-1">
            <span className="w-1 h-1 rounded-full bg-current" />
            {error}
          </p>
        )}
        {!error && helperText && (
          <p className="mt-2 text-sm text-gray-400 dark:text-gray-500 font-medium">{helperText}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };