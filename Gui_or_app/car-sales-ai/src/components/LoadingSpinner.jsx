import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ 
  size = 'md', 
  text = 'Loading...', 
  fullScreen = false,
  overlay = false 
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };

  const spinner = (
    <div className="flex flex-col items-center justify-center space-y-4">
      <Loader2 className={`${sizeClasses[size]} text-secondary animate-spin`} />
      {text && (
        <p className="text-gray-400 text-sm font-medium animate-pulse">
          {text}
        </p>
      )}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-white z-50">
        {spinner}
      </div>
    );
  }

  if (overlay) {
    return (
      <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90 z-40">
        {spinner}
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center py-12">
      {spinner}
    </div>
  );
};

// Progress Spinner with steps
export const ProgressSpinner = ({ steps, currentStep, text }) => {
  return (
    <div className="flex flex-col items-center justify-center space-y-6 py-12">
      <div className="relative">
        <Loader2 className="w-16 h-16 text-secondary animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-sm font-bold text-secondary">
            {currentStep}/{steps.length}
          </span>
        </div>
      </div>
      
      <div className="text-center space-y-2">
        <p className="text-lg font-semibold text-primary">
          {text || 'Processing...'}
        </p>
        <p className="text-sm text-gray-400">
          Step {currentStep} of {steps.length}: {steps[currentStep - 1]}
        </p>
      </div>

      {/* Progress bar */}
      <div className="w-64 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div 
          className="h-full bg-secondary transition-all duration-500"
          style={{ width: `${(currentStep / steps.length) * 100}%` }}
        />
      </div>
    </div>
  );
};

// Skeleton Loader
export const Skeleton = ({ className = '', count = 1, height = 'h-4' }) => {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div 
          key={i}
          className={`${height} bg-gray-200 rounded skeleton ${className}`}
        />
      ))}
    </>
  );
};

export default LoadingSpinner;