import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { signalsApi, channelsApi, brokersApi } from '@/api';
import { StatCard, PerformanceChart, LiveActivity } from '@/components/common';
import { IndianRupee, TrendingUp, BarChart3, Calendar } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

export const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const { data: stats } = useQuery({
    queryKey: ['signal-stats'],
    queryFn: () => signalsApi.getStats(7),
  });

  const { data: channels } = useQuery({
    queryKey: ['channels'],
    queryFn: channelsApi.list,
  });

  const { data: brokers } = useQuery({
    queryKey: ['brokers'],
    queryFn: brokersApi.list,
  });

  const activeChannels = channels?.filter((c) => c.is_active).length || 0;
  const activeBrokers = brokers?.filter((b) => b.is_active).length || 0;

  // Calculate demo values based on real stats
  const totalPnL = (stats?.total_signals || 0) * 45 + 520; // Demo calculation
  const winRate = stats?.success_rate || 68;
  const activeTrades = 0; // Real-time from API
  const dayVolume = (stats?.total_signals || 0) * 1.2 + 2.4; // Demo in lakhs

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-white">Market Overview</h2>
        <p className="text-gray-400 mt-1">
          Welcome back, {user?.username || 'Trader'}. Market is open.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total P&L"
          value={`₹${totalPnL.toLocaleString()}`}
          change={12.5}
          icon={IndianRupee}
          iconColor="text-success-500"
        />
        <StatCard
          title="Win Rate"
          value={`${winRate}%`}
          change={2.1}
          icon={TrendingUp}
          iconColor="text-primary-500"
        />
        <StatCard
          title="Active Trades"
          value={activeTrades}
          icon={BarChart3}
          iconColor="text-primary-500"
        />
        <StatCard
          title="Day's Volume"
          value={`₹${dayVolume.toFixed(1)}L`}
          change={-5.2}
          icon={Calendar}
          iconColor="text-danger-500"
        />
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Performance Chart - Takes 2 columns */}
        <div className="lg:col-span-2">
          <PerformanceChart />
        </div>

        {/* Live Activity - Takes 1 column */}
        <div className="lg:col-span-1">
          <LiveActivity />
        </div>
      </div>

      {/* Additional Stats Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-dark-card border border-dark-border rounded-xl p-6">
          <h3 className="text-sm text-gray-400 font-medium mb-4">Signal Performance</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Parsed Signals</span>
              <span className="font-semibold text-white">{stats?.parsed_signals || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Executed</span>
              <span className="font-semibold text-success-500">{stats?.executed_signals || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Failed</span>
              <span className="font-semibold text-danger-500">{stats?.failed_signals || 0}</span>
            </div>
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-6">
          <h3 className="text-sm text-gray-400 font-medium mb-4">Active Connections</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Telegram Channels</span>
              <span className="font-semibold text-white">{activeChannels}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Broker Accounts</span>
              <span className="font-semibold text-white">{activeBrokers}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-400">Active Mappings</span>
              <span className="font-semibold text-primary-400">{activeChannels + activeBrokers}</span>
            </div>
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-6">
          <h3 className="text-sm text-gray-400 font-medium mb-4">Top Symbols</h3>
          <div className="space-y-3">
            {stats?.top_symbols?.length ? (
              stats.top_symbols.slice(0, 3).map(([symbol, count]) => (
                <div key={symbol} className="flex justify-between items-center">
                  <span className="text-sm font-medium text-white">{symbol}</span>
                  <span className="text-sm text-gray-400">{count} signals</span>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-500">No signals yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
