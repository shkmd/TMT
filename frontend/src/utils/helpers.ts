import { type ClassValue, clsx } from 'clsx';
import { format, formatDistanceToNow } from 'date-fns';

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatDate(date: string | Date): string {
  return format(new Date(date), 'MMM dd, yyyy HH:mm');
}

export function formatRelativeTime(date: string | Date): string {
  return formatDistanceToNow(new Date(date), { addSuffix: true });
}

export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function getBrokerDisplayName(brokerType: string): string {
  const names: Record<string, string> = {
    angel_one: 'Angel One',
    zerodha: 'Zerodha',
    dhan: 'Dhan',
    upstox: 'Upstox',
  };
  return names[brokerType] || brokerType;
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    received: 'text-blue-600 bg-blue-100',
    parsed: 'text-green-600 bg-green-100',
    executing: 'text-yellow-600 bg-yellow-100',
    executed: 'text-green-600 bg-green-100',
    failed: 'text-red-600 bg-red-100',
    ignored: 'text-gray-600 bg-gray-100',
  };
  return colors[status] || 'text-gray-600 bg-gray-100';
}
