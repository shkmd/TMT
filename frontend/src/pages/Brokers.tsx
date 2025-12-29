import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { brokersApi } from '@/api';
import { Card, Button, Input } from '@/components/common';
import { BrokerCreate, BrokerType } from '@/types/api';
import { Plus, Trash2, Briefcase } from 'lucide-react';
import toast from 'react-hot-toast';
import { getBrokerDisplayName, formatDate } from '@/utils/helpers';

export const Brokers: React.FC = () => {
  const queryClient = useQueryClient();
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<BrokerCreate>({
    broker_type: 'angel_one',
    broker_name: '',
    api_key: '',
    client_id: '',
    is_active: true,
  });

  const { data: brokers, isLoading } = useQuery({
    queryKey: ['brokers'],
    queryFn: brokersApi.list,
  });

  const createMutation = useMutation({
    mutationFn: brokersApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['brokers'] });
      toast.success('Broker added successfully');
      setShowForm(false);
      setFormData({
        broker_type: 'angel_one',
        broker_name: '',
        api_key: '',
        client_id: '',
        is_active: true,
      });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to add broker');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: brokersApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['brokers'] });
      toast.success('Broker deleted successfully');
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
          <h2 className="text-3xl font-bold text-gray-900">Brokers</h2>
          <p className="text-gray-600 mt-1">Manage broker integrations</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          <Plus size={18} className="mr-2" />
          Add Broker
        </Button>
      </div>

      {showForm && (
        <Card title="Add New Broker">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Broker Type</label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                value={formData.broker_type}
                onChange={(e) => setFormData({ ...formData, broker_type: e.target.value as BrokerType })}
              >
                <option value="angel_one">Angel One</option>
                <option value="zerodha">Zerodha</option>
                <option value="dhan">Dhan</option>
                <option value="upstox">Upstox</option>
              </select>
            </div>
            <Input
              label="Broker Name"
              placeholder="My Trading Account"
              value={formData.broker_name}
              onChange={(e) => setFormData({ ...formData, broker_name: e.target.value })}
              required
            />
            <Input
              label="API Key"
              placeholder="Enter API key"
              value={formData.api_key}
              onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
            />
            <Input
              label="Client ID"
              placeholder="Enter client ID"
              value={formData.client_id}
              onChange={(e) => setFormData({ ...formData, client_id: e.target.value })}
            />
            <div className="flex space-x-3">
              <Button type="submit" isLoading={createMutation.isPending}>
                Add Broker
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
      ) : brokers?.length ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {brokers.map((broker) => (
            <Card key={broker.id}>
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Briefcase size={20} className="text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{broker.broker_name}</h3>
                    <p className="text-sm text-gray-600">{getBrokerDisplayName(broker.broker_type)}</p>
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                      <span>Added {formatDate(broker.created_at)}</span>
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        broker.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {broker.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                    <div className="mt-2 text-xs text-gray-500">
                      {broker.has_api_key && '🔑 API Key configured'}
                    </div>
                  </div>
                </div>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => {
                    if (confirm('Delete this broker?')) {
                      deleteMutation.mutate(broker.id);
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
            <Briefcase size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600">No brokers yet. Add your first broker to start trading.</p>
          </div>
        </Card>
      )}
    </div>
  );
};
