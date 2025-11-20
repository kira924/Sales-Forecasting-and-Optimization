import React, { useState } from 'react';
import { Info } from 'lucide-react';

const Tooltip = ({ 
  children, 
  content, 
  position = 'top',
  showIcon = true,
  iconSize = 'sm'
}) => {
  const [isVisible, setIsVisible] = useState(false);

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  const arrowClasses = {
    top: 'top-full left-1/2 -translate-x-1/2 border-t-gray-500',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-b-gray-500',
    left: 'left-full top-1/2 -translate-y-1/2 border-l-gray-500',
    right: 'right-full top-1/2 -translate-y-1/2 border-r-gray-500',
  };

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  return (
    <div className="relative inline-flex items-center">
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        className="cursor-help inline-flex items-center"
      >
        {showIcon ? (
          <Info className={`${iconSizes[iconSize]} text-gray-400 hover:text-secondary transition-colors`} />
        ) : (
          children
        )}
      </div>

      {isVisible && (
        <div className={`
          absolute ${positionClasses[position]} z-50
          px-3 py-2 text-sm text-white bg-gray-500 rounded-lg
          shadow-lg whitespace-nowrap max-w-xs
          animate-fade-in
        `}>
          {content}
          <div className={`
            absolute ${arrowClasses[position]}
            border-4 border-transparent
          `} />
        </div>
      )}
    </div>
  );
};

export default Tooltip;