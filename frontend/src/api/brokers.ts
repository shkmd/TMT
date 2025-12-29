import axiosInstance from './axios';
import { Broker, BrokerCreate, BrokerUpdate, ChannelBrokerMapping, ChannelBrokerMappingCreate } from '@/types/api';

export const brokersApi = {
  async list(): Promise<Broker[]> {
    const response = await axiosInstance.get<Broker[]>('/brokers/');
    return response.data;
  },

  async get(id: number): Promise<Broker> {
    const response = await axiosInstance.get<Broker>(`/brokers/${id}`);
    return response.data;
  },

  async create(data: BrokerCreate): Promise<Broker> {
    const response = await axiosInstance.post<Broker>('/brokers/', data);
    return response.data;
  },

  async update(id: number, data: BrokerUpdate): Promise<Broker> {
    const response = await axiosInstance.put<Broker>(`/brokers/${id}`, data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await axiosInstance.delete(`/brokers/${id}`);
  },

  // Mappings
  async listMappings(params?: { channel_id?: number; broker_id?: number }): Promise<ChannelBrokerMapping[]> {
    const response = await axiosInstance.get<ChannelBrokerMapping[]>('/brokers/mappings', { params });
    return response.data;
  },

  async createMapping(data: ChannelBrokerMappingCreate): Promise<ChannelBrokerMapping> {
    const response = await axiosInstance.post<ChannelBrokerMapping>('/brokers/mappings', data);
    return response.data;
  },

  async deleteMapping(id: number): Promise<void> {
    await axiosInstance.delete(`/brokers/mappings/${id}`);
  },
};
