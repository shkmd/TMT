import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { brokersApi, channelsApi } from '@/api';
import { Card, Button } from '@/components/common';
import { ChannelBrokerMappingCreate } from '@/types/api';
import { Plus, Trash2, LinkIcon } from 'lucide-react';
import toast from 'react-hot-toast';
import { getBrokerDisplayName } from '@/utils/helpers';

export const Mappings: React.FC = () => {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<ChannelBrokerMappingCreate>({
    telegram_channel_id: 0,
    broker_id: 0,
    is_active: true,
  });

  const { data: mappings } = useQuery({
    queryKey: ['mappings'],
    queryFn: () => brokersApi.listMappings(),
  });

  const { data: channels } = useQuery({
    queryKey: ['channels'],
    queryFn: channelsApi.list,
  });

  const { data: brokers } = useQuery({
    queryKey: ['brokers'],
    queryFn: brokersApi.list,
  });

  const createMutation = useMutation({
    mutationFn: brokersApi.createMapping,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mappings'] });
      toast.success('Mapping created successfully');
      setShowForm(false);
      setFormData({ telegram_channel_id: 0, broker_id: 0, is_active: true });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create mapping');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: brokersApi.deleteMapping,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mappings'] });
      toast.success('Mapping deleted successfully');
    },
  });

  const getChannelName = (id: number) => channels?.find((c) => c.id === id)?.channel_name || 'Unknown';
  const getBrokerName = (id: number) => {
    const broker = brokers?.find((b) => b.id === id);
    return broker ? `${broker.broker_name} (${getBrokerDisplayName(broker.broker_type)})` : 'Unknown';
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Channel-Broker Mappings</h2>
          <p className="text-gray-600 mt-1">Route signals from channels to brokers</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus size={18} className="mr-2" />
          Add Mapping
        </Button>
      </div>

      {showForm && (
        <Card title="Create New Mapping">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Telegram Channel</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                value={formData.telegram_channel_id}
                onChange={(e) => setFormData({ ...formData, telegram_channel_id: parseInt(e.target.value) })}
                required
              >
                <option value={0}>Select a channel</option>
                {channels?.map((channel) => (
                  <option key={channel.id} value={channel.id}>
                    {channel.channel_name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Broker</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                value={formData.broker_id}
                onChange={(e) => setFormData({ ...formData, broker_id: parseInt(e.target.value) })}
                required
              >
                <option value={0}>Select a broker</option>
                {brokers?.map((broker) => (
                  <option key={broker.id} value={broker.id}>
                    {broker.broker_name} ({getBrokerDisplayName(broker.broker_type)})
                  </option>
                ))}
              </select>
            </div>
            <div className="flex space-x-3">
              <Button type="submit" isLoading={createMutation.isPending}>
                Create Mapping
              </Button>
              <Button variant="ghost" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {mappings?.length ? (
        <div className="space-y-3">
          {mappings.map((mapping) => (
            <Card key={mapping.id}>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  <div className="p-2 bg-primary-100 rounded-lg">
                    <LinkIcon size={20} className="text-primary-600" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-3">
                      <span className="font-medium text-gray-900">
                        {getChannelName(mapping.telegram_channel_id)}
                      </span>
                      <span className="text-gray-400">→</span>
                      <span className="font-medium text-gray-900">
                        {getBrokerName(mapping.broker_id)}
                      </span>
                    </div>
                    <span className={`inline-block mt-2 px-2 py-0.5 rounded-full text-xs font-medium ${
                      mapping.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {mapping.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => {
                    if (confirm('Delete this mapping?')) {
                      deleteMutation.mutate(mapping.id);
                    }
                  }}
                >
                  <Trash2 size={16} />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <div className="text-center py-12">
            <LinkIcon size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600">No mappings yet. Create mappings to route signals to brokers.</p>
          </div>
        </Card>
      )}
    </div>
  );
};
