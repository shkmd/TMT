import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Radio, Briefcase, Activity, LinkIcon } from 'lucide-react';
import { cn } from '@/utils/helpers';

const navigation = [
  { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
  { name: 'Channels', to: '/channels', icon: Radio },
  { name: 'Brokers', to: '/brokers', icon: Briefcase },
  { name: 'Signals', to: '/signals', icon: Activity },
  { name: 'Mappings', to: '/mappings', icon: LinkIcon },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-gray-900 min-h-screen">
      <nav className="mt-8 px-4">
        <div className="space-y-1">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  'flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors',
                  isActive
                    ? 'bg-gray-800 text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                )
              }
            >
              <item.icon className="mr-3 h-5 w-5" />
              {item.name}
            </NavLink>
          ))}
        </div>
      </nav>
    </aside>
  );
};
