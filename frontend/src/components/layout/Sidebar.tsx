import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  TrendingUp,
  Radio,
  Sparkles,
  CreditCard,
  Settings,
  Activity
} from 'lucide-react';
import { cn } from '@/utils/helpers';

const mainNavigation = [
  { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { name: 'Trade History', to: '/signals', icon: TrendingUp },
  { name: 'Connections', to: '/channels', icon: Radio },
  { name: 'AI Signal Lab', to: '/ai-lab', icon: Sparkles },
  { name: 'Subscription', to: '/subscription', icon: CreditCard },
];

const bottomNavigation = [
  { name: 'Settings', to: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-dark-surface min-h-screen flex flex-col border-r border-dark-border">
      {/* Logo/Branding */}
      <div className="flex items-center gap-2 px-6 py-6">
        <div className="w-8 h-8 bg-gradient-to-br from-primary-400 to-primary-600 rounded-lg flex items-center justify-center">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <span className="text-xl font-bold text-white">TradeSync.AI</span>
      </div>

      {/* Main Navigation */}
      <nav className="flex-1 px-4 mt-4">
        <div className="space-y-1">
          {mainNavigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200',
                  isActive
                    ? 'bg-primary-500/10 text-primary-400 border-l-4 border-primary-500'
                    : 'text-gray-400 hover:bg-dark-hover hover:text-gray-200'
                )
              }
            >
              <item.icon className="h-5 w-5" />
              {item.name}
            </NavLink>
          ))}
        </div>
      </nav>

      {/* Bottom Navigation */}
      <div className="px-4 pb-6">
        <div className="border-t border-dark-border pt-4">
          {bottomNavigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200',
                  isActive
                    ? 'bg-primary-500/10 text-primary-400'
                    : 'text-gray-400 hover:bg-dark-hover hover:text-gray-200'
                )
              }
            >
              <item.icon className="h-5 w-5" />
              {item.name}
            </NavLink>
          ))}
        </div>
      </div>
    </aside>
  );
};
