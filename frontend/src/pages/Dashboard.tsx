import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { signalsApi, channelsApi, brokersApi } from '@/api';
import { Card } from '@/components/common';
import { Activity, Radio, Briefcase, TrendingUp } from 'lucide-react';
import { formatRelativeTime } from '@/utils/helpers';

const StatCard: React.FC<{
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, icon, color }) => (
  <Card>
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
      </div>
      <div className={`p-3 rounded-full ${color}`}>{icon}</div>
    </div>
  </Card>
);

export const Dashboard: React.FC = () => {
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

  const { data: latestSignals } = useQuery({
    queryKey: ['latest-signals'],
    queryFn: () => signalsApi.getLatest(5),
  });

  const activeChannels = channels?.filter((c) => c.is_active).length || 0;
  const activeBrokers = brokers?.filter((b) => b.is_active).length || 0;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-600 mt-1">Overview of your trading automation</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Signals (7d)"
          value={stats?.total_signals || 0}
          icon={<Activity size={24} className="text-primary-600" />}
          color="bg-primary-100"
        />
        <StatCard
          title="Active Channels"
          value={activeChannels}
          icon={<Radio size={24} className="text-green-600" />}
          color="bg-green-100"
        />
        <StatCard
          title="Active Brokers"
          value={activeBrokers}
          icon={<Briefcase size={24} className="text-blue-600" />}
          color="bg-blue-100"
        />
        <StatCard
          title="Success Rate"
          value={`${stats?.success_rate || 0}%`}
          icon={<TrendingUp size={24} className="text-purple-600" />}
          color="bg-purple-100"
        />
      </div>

      {/* Performance Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Signal Performance">
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Parsed Signals</span>
              <span className="font-semibold">{stats?.parsed_signals || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Executed Signals</span>
              <span className="font-semibold">{stats?.executed_signals || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Failed Signals</span>
              <span className="font-semibold text-red-600">{stats?.failed_signals || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Execution Rate</span>
              <span className="font-semibold">{stats?.execution_rate || 0}%</span>
            </div>
          </div>
        </Card>

        <Card title="Top Symbols">
          <div className="space-y-3">
            {stats?.top_symbols?.length ? (
              stats.top_symbols.slice(0, 5).map(([symbol, count]) => (
                <div key={symbol} className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-900">{symbol}</span>
                  <span className="text-sm text-gray-600">{count} signals</span>
                </div>
              ))
            ) : (
              <p className="text-sm text-gray-500">No signals yet</p>
            )}
          </div>
        </Card>
      </div>

      {/* Latest Signals */}
      <Card title="Latest Signals">
        {latestSignals?.length ? (
          <div className="space-y-3">
            {latestSignals.map((signal) => (
              <div
                key={signal.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{signal.symbol || 'Unknown'}</p>
                  <p className="text-sm text-gray-600">
                    {signal.order_type?.toUpperCase()} • {signal.action?.toUpperCase()}
                  </p>
                </div>
                <div className="text-right">
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full ${
                      signal.status === 'executed'
                        ? 'bg-green-100 text-green-800'
                        : signal.status === 'failed'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}
                  >
                    {signal.status}
                  </span>
                  <p className="text-xs text-gray-500 mt-1">
                    {signal.received_at && formatRelativeTime(signal.received_at)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">No signals yet</p>
        )}
      </Card>
    </div>
  );
};
