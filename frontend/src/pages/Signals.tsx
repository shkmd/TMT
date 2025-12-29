import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { signalsApi } from '@/api';
import { Card } from '@/components/common';
import { Activity } from 'lucide-react';
import { formatDate, getStatusColor } from '@/utils/helpers';

export const Signals: React.FC = () => {
  const { data: signals, isLoading } = useQuery({
    queryKey: ['signals'],
    queryFn: () => signalsApi.list({ limit: 50 }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Trading Signals</h2>
        <p className="text-gray-600 mt-1">Monitor all trading signals</p>
      </div>

      {isLoading ? (
        <div className="text-center py-12">Loading...</div>
      ) : signals?.length ? (
        <Card>
          <div className="space-y-3">
            {signals.map((signal) => (
              <div
                key={signal.id}
                className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <h3 className="font-semibold text-gray-900 text-lg">
                        {signal.symbol || 'Unknown Symbol'}
                      </h3>
                      {signal.order_type && (
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          signal.order_type === 'buy' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {signal.order_type.toUpperCase()}
                        </span>
                      )}
                      {signal.action && (
                        <span className="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                          {signal.action.toUpperCase()}
                        </span>
                      )}
                    </div>

                    <div className="grid grid-cols-3 gap-4 mt-3 text-sm">
                      {signal.entry_price && (
                        <div>
                          <span className="text-gray-600">Entry:</span>
                          <span className="font-medium ml-2">₹{signal.entry_price}</span>
                        </div>
                      )}
                      {signal.target_price && (
                        <div>
                          <span className="text-gray-600">Target:</span>
                          <span className="font-medium ml-2">₹{signal.target_price}</span>
                        </div>
                      )}
                      {signal.stoploss_price && (
                        <div>
                          <span className="text-gray-600">SL:</span>
                          <span className="font-medium ml-2">₹{signal.stoploss_price}</span>
                        </div>
                      )}
                    </div>

                    {signal.raw_message && (
                      <div className="mt-3 p-2 bg-white rounded text-xs text-gray-600 font-mono">
                        {signal.raw_message.slice(0, 150)}
                        {signal.raw_message.length > 150 && '...'}
                      </div>
                    )}

                    <div className="mt-3 text-xs text-gray-500">
                      Received {formatDate(signal.received_at)}
                    </div>
                  </div>

                  <span className={`px-3 py-1 text-xs font-medium rounded-full ${getStatusColor(signal.status)}`}>
                    {signal.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      ) : (
        <Card>
          <div className="text-center py-12">
            <Activity size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600">No signals yet. Configure channels to start receiving signals.</p>
          </div>
        </Card>
      )}
    </div>
  );
};
