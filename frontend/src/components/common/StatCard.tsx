import React from 'react';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { cn } from '../../utils/helpers';

interface StatCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon: LucideIcon;
  iconColor?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  change,
  changeLabel = 'vs yesterday',
  icon: Icon,
  iconColor = 'text-primary-500',
}) => {
  const isPositive = change !== undefined && change >= 0;
  const showChange = change !== undefined;

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-6 hover:bg-dark-hover transition-all duration-200">
      {/* Header with Title and Icon */}
      <div className="flex items-start justify-between mb-4">
        <div className="text-sm text-gray-400 font-medium">{title}</div>
        <div className={cn('p-2 rounded-lg bg-dark-surface', iconColor)}>
          <Icon className="h-5 w-5" />
        </div>
      </div>

      {/* Value */}
      <div className="text-3xl font-bold text-white mb-2">{value}</div>

      {/* Change Indicator */}
      {showChange && (
        <div className="flex items-center gap-1 text-sm">
          {isPositive ? (
            <TrendingUp className="h-4 w-4 text-success-500" />
          ) : (
            <TrendingDown className="h-4 w-4 text-danger-500" />
          )}
          <span className={isPositive ? 'text-success-500' : 'text-danger-500'}>
            {isPositive ? '+' : ''}
            {change}%
          </span>
          <span className="text-gray-500">{changeLabel}</span>
        </div>
      )}
    </div>
  );
};
