import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { channelsApi } from '@/api';
import { Card, Button, Input } from '@/components/common';
import { TelegramChannelCreate } from '@/types/api';
import { Plus, Trash2, Radio } from 'lucide-react';
import toast from 'react-hot-toast';
import { formatDate } from '@/utils/helpers';

export const Channels: React.FC = () => {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<TelegramChannelCreate>({
    channel_name: '',
    description: '',
    is_active: true,
  });

  const { data: channels, isLoading } = useQuery({
    queryKey: ['channels'],
    queryFn: channelsApi.list,
  });

  const createMutation = useMutation({
    mutationFn: channelsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['channels'] });
      toast.success('Channel added successfully');
      setShowForm(false);
      setFormData({ channel_name: '', description: '', is_active: true });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to add channel');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: channelsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['channels'] });
      toast.success('Channel deleted successfully');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Telegram Channels</h2>
          <p className="text-gray-600 mt-1">Manage trading signal channels</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus size={18} className="mr-2" />
          Add Channel
        </Button>
      </div>

      {showForm && (
        <Card title="Add New Channel">
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Channel Name"
              placeholder="@trading_signals or channel ID"
              value={formData.channel_name}
              onChange={(e) => setFormData({ ...formData, channel_name: e.target.value })}
              required
            />
            <Input
              label="Description"
              placeholder="Optional description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
            <div className="flex space-x-3">
              <Button type="submit" isLoading={createMutation.isPending}>
                Add Channel
              </Button>
              <Button variant="ghost" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
            </div>
          </form>
        </Card>
      )}

      {isLoading ? (
        <div className="text-center py-12">Loading...</div>
      ) : channels?.length ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {channels.map((channel) => (
            <Card key={channel.id}>
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <div className="p-2 bg-primary-100 rounded-lg">
                    <Radio size={20} className="text-primary-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{channel.channel_name}</h3>
                    {channel.description && (
                      <p className="text-sm text-gray-600 mt-1">{channel.description}</p>
                    )}
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                      <span>Added {formatDate(channel.created_at)}</span>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        channel.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {channel.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                </div>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => {
                    if (confirm('Delete this channel?')) {
                      deleteMutation.mutate(channel.id);
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
            <Radio size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600">No channels yet. Add your first channel to start monitoring signals.</p>
          </div>
        </Card>
      )}
    </div>
  );
};
