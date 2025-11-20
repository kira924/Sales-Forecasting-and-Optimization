import React from 'react';
import classNames from 'classnames';

const Card = ({
  children,
  title,
  subtitle,
  icon,
  bordered = false,
  hoverable = true,
  className = '',
  headerAction,
  footer,
  ...props
}) => {
  const cardClasses = classNames(
    'bg-white rounded-lg p-6',
    bordered ? 'border-2 border-gray-100' : 'shadow-md',
    hoverable && (bordered ? 'hover:border-secondary' : 'hover:shadow-lg'),
    'transition-all duration-250',
    className
  );

  return (
    <div className={cardClasses} {...props}>
      {/* Header */}
      {(title || icon || headerAction) && (
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            {icon && (
              <div className="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-secondary-light text-white rounded-lg">
                {icon}
              </div>
            )}
            <div>
              {title && (
                <h3 className="text-lg font-semibold text-primary">
                  {title}
                </h3>
              )}
              {subtitle && (
                <p className="text-sm text-gray-400 mt-1">
                  {subtitle}
                </p>
              )}
            </div>
          </div>
          {headerAction && (
            <div className="flex-shrink-0">
              {headerAction}
            </div>
          )}
        </div>
      )}

      {/* Content */}
      <div className="text-gray-500">
        {children}
      </div>

      {/* Footer */}
      {footer && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          {footer}
        </div>
      )}
    </div>
  );
};

// Stat Card variant
export const StatCard = ({
  title,
  value,
  change,
  changeType = 'neutral',
  icon,
  color = 'primary',
  loading = false,
}) => {
  const colorClasses = {
    primary: 'border-secondary',
    success: 'border-success',
    warning: 'border-warning',
    danger: 'border-danger',
  };

  const changeColors = {
    positive: 'text-success',
    negative: 'text-danger',
    neutral: 'text-gray-400',
  };

  if (loading) {
    return (
      <div className={`stat-card ${colorClasses[color]} animate-pulse`}>
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
            <div className="h-8 bg-gray-200 rounded w-32"></div>
          </div>
          {icon && <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>}
        </div>
      </div>
    );
  }

  return (
    <div className={`stat-card ${colorClasses[color]}`}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-400 mb-1">
            {title}
          </p>
          <p className="text-3xl font-bold text-primary">
            {value}
          </p>
          {change !== undefined && (
            <p className={`text-sm font-medium mt-2 ${changeColors[changeType]}`}>
              {change > 0 ? '↑' : change < 0 ? '↓' : '→'} {Math.abs(change)}%
            </p>
          )}
        </div>
        {icon && (
          <div className={`w-12 h-12 flex items-center justify-center bg-${color}-light text-white rounded-lg`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  );
};

export default Card;