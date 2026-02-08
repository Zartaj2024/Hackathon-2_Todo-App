import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  subtitle?: string;
  variant?: 'default' | 'elevated' | 'outlined' | 'glass';
  size?: 'sm' | 'md' | 'lg';
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ title, subtitle, variant = 'default', size = 'md', children, className = '', ...props }, ref) => {
    const variantClasses = {
      default: 'bg-white border border-gray-100 dark:bg-slate-900/40 dark:border-gray-800',
      elevated: 'bg-white shadow-premium dark:bg-slate-900 dark:border-gray-800',
      outlined: 'bg-transparent border-2 border-gray-100 dark:border-gray-800',
      glass: 'glass-card',
    };

    const sizeClasses = {
      sm: 'rounded-xl',
      md: 'rounded-2xl',
      lg: 'rounded-3xl',
    };

    const paddingClasses = size === 'sm' ? 'p-4' : size === 'lg' ? 'p-10' : 'p-7';

    return (
      <div
        ref={ref}
        className={`transition-all duration-300 ease-in-out overflow-hidden shadow-sm ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
        {...props}
      >
        {(title || subtitle) && (
          <div className={`${paddingClasses} pb-3`}>
            {title && (
              <h3 className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">{title}</h3>
            )}
            {subtitle && (
              <p className="mt-1 text-sm font-medium text-gray-500 dark:text-gray-400">{subtitle}</p>
            )}
          </div>
        )}
        <div className={paddingClasses}>
          {children}
        </div>
      </div>
    );
  }
);

Card.displayName = 'Card';

export { Card };